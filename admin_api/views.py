from ast import Delete
from telnetlib import STATUS
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from bson import ObjectId
from tiktik.settings import db
from .validation import *
import datetime
# Create your views here.
class AdminUserAdd(APIView):
     
    def get(self, request):
        ''' check datas
        1 for user
        2 for phoneNumber
        '''
        token = request.META['HTTP_AUTHORIZATION'] if "HTTP_AUTHORIZATION" in request.META else ""
        if token == "":
            pass
        else:
            
            user_name = request.META['HTTP_USERNAME'] if 'HTTP_USERNAME' in request.META else ""
            password = request.META['HTTP_PASSWORD'] if 'HTTP_PASSWORD' in request.META else ""
            try:
                type = int(request.GET.get('type' , 3))
            except:
                type = 3
             
            if user_name == "":
                response_data= {'message': 'enter valide userName'}
                return JsonResponse(response_data, safe=False,status=422)
            
            if type == 3:
                response_data= {'message': 'plz enter valide value'}
                return JsonResponse(response_data, status=422)
            if type ==1:
                if password == "":
                    response_data= {'message': 'enter valide password'}
                    return JsonResponse(response_data, status=422)
                
                else:
                    ''' check that '''
                    check = db.UserDetail.find_one({'userName':user_name})
                    if check is not None:
                        print(password)
                        check_password = db.UserDetail.find_one({'userName':user_name , "passWord":password})
                        if check_password is not None:
                            value = {
                                'name': check_password['firstName'] + ' ' + check_password['lastName'],
                                'read':check_password['readPermission'],
                                'write': check_password['writePermission']
                            }
                            response_data = {'message':'data found' , 'data':value}
                            return JsonResponse(response_data,safe=False, status=200)
                        else:
                            response_data= {'message': 'plz enter valide password'}
                            return JsonResponse(response_data, status=404)
                    else:
                        response_data= {'message': 'plz enter valide Email or PhoneNumber'}
                        return JsonResponse(response_data, status=404)
            else:
                phone_number = user_name
                find_number = db.UserDetail.find_one({"phoneNumber": phone_number})
                if find_number is None:
                    pass
                else:
                    
                    response_data= {'message': 'plz enter valide Email or PhoneNumber'}
                    return JsonResponse(response_data, status=404)
    
    def post(self, request):
        data = request.data
        ''' validate Data '''
        if "firstName" not in data or data['firstName'] == "":
            response_data = {'message':'Enter first name'}
            return JsonResponse(response_data, status=422)
        elif "firstName" not in data or data['firstName'] == "":
            response_data = {'message': 'Enter last name'}
            return JsonResponse(response_data, status=422)
        elif "userName" not in data or data['userName'] == "":
            response_data = {'message': 'Enter userName'}
            return JsonResponse(response_data, status=422)
        elif "email" not in data or data['email'] == "":
            response_data = {'message': 'Enter email'}
            return JsonResponse(response_data, status=422)
        elif "phoneNumber" not in data or data['phoneNumber'] == "":
            response_data = {'message': 'Enter phone number'}
            return JsonResponse(response_data, status=422)
        elif "passWord" not in data or data['passWord'] == "":
            response_data = {'message': 'Enter password'}
            return JsonResponse(response_data, status=422)
        elif "address" not in data or data['address'] == []:
            response_data = {'message': 'Enter address'}
            return JsonResponse(response_data, status=422)
        elif "city" not in data or data['city'] == "":
            response_data = {'message': 'Enter city'}
            return JsonResponse(response_data, status=422)
        elif "Country" not in data or data['Country'] == "":
            response_data = {'message': 'Enter Country'}
            return JsonResponse(response_data, status=422)
        elif "state" not in data or data['state'] == "":
            response_data = {'message': 'Enter state'}
            return JsonResponse(response_data, status=422)
        else:
            query = {
                "firstName": data["firstName"],
                "lastName": data["LastName"],
                "photo": data['photo'] if 'photo' in data else "",
                "userName": data['userName'],
                "email": data["email"],
                "stauts": 1,
                "phoneNumber": int(data["phoneNumber"]),
                "passWord": data["passWord"],
                "readPermission": data["readPermission"] if "readPermission" in data else 0,
                "writePermission": data["writePermission"] if "writePermission" in data else 0,
                "address": data["address"],
                "state":data['state'].upper(),
                "city" : data["city"].upper(),
                "Country": data["Country"].upper()
                
            }
            print(query)
            db.UserDetail.insert_one(query)
            response_data = {'messgae': 'data add succesfully'}
            return JsonResponse(response_data, status=200)

class CheckUserData(APIView):
    def get(self, request):
        value = request.META['HTTP_VALUE'] if 'HTTP_VALUE' in request.META else ""
        field = request.GET.get('field' , "")
        result = user_data_check(field, value)
        if result == 0:
            response_data = {'messgae': field + ' add successfully'}
            return JsonResponse(response_data, STATUS=200)
        else:
            response_data = {'messgae': field + ' already register'}
            return JsonResponse(response_data, STATUS=422)

class PersonDetail(APIView):
    def get(self, request):
        ids = request.META['HTTP_ID'] if "HTTP_ID" in request.META else ""
        if ids == "":
            resopnse_data = {'messgae': 'something went wrongs'}
            return JsonResponse(resopnse_data, status=422)
        else:
            ''' find Data '''
            data = db.UserDetail.find_one({"_id": ObjectId(ids)})
            if data is None:
                response_data = {'data': [], 'messgae':'user not found'}
                return JsonResponse(response_data, status=200)
            else:
                result = [{
                "id": str(data["_id"]),
                "firstName": data["firstName"],
                "lastName": data["lastName"],
                "photo": data['photo'] if 'photo' in data else "",
                "userName": data['userName'],
                "email": data["email"],
                "phoneNumber": data["phoneNumber"],
                # "password": data["passWord"],
                "readPermission": data["readPermission"] if "readPermission" in data else 0,
                "writePermission": data["writePermission"] if "writePermission" in data else 0,
                "address": data["address"],
                "city" : data["city"],
                "Country": data["Country"]
            }]
            response_data = {'data': result, 'messgae':'user found'}
            return JsonResponse(response_data, status=200)

class UserDetail(APIView):
    def get(self, request):
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', 20))
        search = request.GET.get('search', "")
        sort = request.GET.get('sort', '')
        status = int(request.GET.get('status', 1))
        value_sort = request.GET.get('value', '')
        fsort = 'des'
        print(sort)
        ''' check search '''
        query = {'status':status}
        if search != "":
            query = query['$or'] = [{"firstName":search, "lastName": search}]
        sort_data = ""
        if sort != "":
            spit_data = sort.split('_')
            sort_data = spit_data[1]
            fsort = spit_data[0]
            if sort_data == "city":
                query['city'] = value_sort
            elif sort_data == "Country":
                query['Country'] = value_sort
            elif sort_data == 'status':
                query['status'] = value_sort

        sort_query = 1 if fsort == 'asc' else -1
        print('query->',query)
        final_data = db.UserDetail.find(query).skip(skip).limit(limit).sort([('_id', sort_query)])
        final_data_count =  db.UserDetail.count_documents(query)
        final_list = []
        if final_data is not None:
            for data in final_data:
                print('datas----->',data)
                final_list.append(
                    {
                        "id": str(data["_id"]),
                        "name": data["firstName"] + " " +data["lastName"],
                        "photo": data['photo'] if 'photo' in data else "",
                        "userName": data['userName'],
                        "email": data["email"],
                        "phoneNumber": data["phoneNumber"],
                        "passWord": data["passWord"],
                        "readPermission": data["readPermission"] if "readPermission" in data else 0,
                        "writePermission": data["writePermission"] if "writePermission" in data else 0,
                        "address": data["address"],
                        "city" : data["city"],
                        "Country": data["Country"]
                    }
                )
            response_data = {'message':"data found", "data":final_list, "penCount": final_data_count}
            return JsonResponse(response_data, status=200)
        else:
            response_data = {'message':"data not found", "data":final_data, "penCOunt":0}
            return JsonResponse(response_data, status=404)

class AdminCategory(APIView):
    def get(self, request):
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', 20))
        # name = request.GET.get('cname', "")
        lan = request.GET.get('language', "en")
        try:
            status = int(request.GET.get('status' , 0))
        except:
            status = 1
        search = request.GET.get('search', "")
        query = {'status':status}
        final_list = []
        if search != "":
            data_name = "categoryName" + '.' + lan
            query[data_name] = { '$regex' : search, '$options': 'i' }
        print(query)
        find_data_count = db.categoryMain.count_documents(query)
        if find_data_count < 1:
            response_data = {'message': 'data not found'}
            return JsonResponse(response_data, status=404)
        else:
            final_data = db.categoryMain.find(query)
            for data in final_data:
                # date = datetime.datetime.strptime(data['createOn'], '%Y-%m-%d')
                final_list.append(
                    {
                    "categoryName": data['categoryName'],
                    'categoryPic': data['categoryPic'] if 'categoryPic' in data else "",
                    'createOn': data['createOn'],
                    'status': data['status']
                    }
                )
            response_data = {'message':'data found', 'data':final_list}
            return JsonResponse(response_data, status=200)


    def post(self, request):
        '''
        type
        1 normal
        2 business
        3 star

        '''
        data = request.data
        if 'categoryName' not in data or len(data['categoryName']) < 0:
            response = {'message': 'Enter Category Name'}
            return JsonResponse(response, status=422)
        else:
            # ln = data['language'] if 'language' else 'en'
            # name_data = 'categoryName.' + ln
            check_cat = db.categoryMain.count_documents({'categoryName':data['categoryName']})
            typ = data['type'] if 'type' in data else 1
            if check_cat > 0:
                pass
            else:
                query = {
                    'categoryName': data['categoryName'],
                    'categoryPic': data['categoryPic'] if 'categoryPic' in data else "",
                    'createOn': datetime.datetime.now(),
                    'status':0,
                    'type': 1
                }
                db.categoryMain.insert_one(query)
                response_data = {'message': "category added"}
                return JsonResponse(response_data, status=200)
    ''' banner '''
class BannerDetail(APIView):
    '''
    0 : pendding
    1 : active
    2 : inactive
    3 : delete
    '''
    def get(self, request):
        try:
            status = int(request.GET.get('status', 0))
        except:
            status = 0
        bname = request.GET.get('bName', "")
        city = request.GET.get('city', "")
        country = request.GET.get('country', "")
        query = {'status': status}
        try:
            skip = int(request.GET.get('skip' , 0))
            limit = int(request.GET.get('limit' , 20))
        except:
            skip = 0
            limit = 20
        if bname != "":
            query['bName'] = bname
        if city != "":
            query['city'] = city
        if country['country'] != "":
            query['country'] = country
        banner_data = db.banner.find(query).sort([('_id', -1)]).skip(skip).limit(limit)
        banner_data_count = db.banner.count_documents(query).sort([('_id', -1)])
        if banner_data_count == 0:
            response_data = {'messgae':"data not found", 'data':[], 'penCount':0 }
            return JsonResponse(response_data, status = 404, safe= False)
        else:
            final_list = []
            for data in banner_data:
                final_list.append(
                    {
                        "id": str(data['_id']),
                        "bannerName": data['bName'],
                        "createOn": data['createOn'],
                        "city" : data['city'],
                        "country": data['country'],
                        "status": data['status'],
                    }
                )
            response_data = {'message': 'data found', 'data' : final_list, 'penCount': banner_data_count}
            return JsonResponse(response_data, status = 200, safe= False)
                
                
        
                        
    
    def post(self, request):
        data = request.data
        if 'bName' not in data:
            pass
        elif data['bName'] == "":
            pass
        elif 'bImage' not in data and data['bImage'] == "":
            pass
        elif 'city' not in data and data['city'] =="":
            pass
        elif 'country' not in "country" and data['country'] == "":
            pass
        else: 
            query = {
                'bName': data['bName'],
                'bImage': data['bImage'],
                'city': data['city'],
                'country': data['country'],
                "createOn": datetime.datetime.now().isoformat(),
                "status": 0
            }    
            db.banner.insert(query)
            response_data = {'messgae': 'banner added successfilly'}
            return JsonResponse(response_data, status=200)
        
    
    def patch(self, request):
        data = request.data
        status = data['status'] if 'status' in data else 0
        query = {'status':status}
        if 'bName' in data and data['bName'] != "":
            query['bName'] = data['bName']
        elif 'bImage' in data and data['bImage'] != "":
            query['bImage'] = data['bImage']
        elif 'city' in data and data['city'] != "":
            query['city'] = data['city']
        elif 'country' in data and data['country'] != "":
            query['country'] = data['country']
        else: 
            db.banner.insert(query)
            response_data = {'messgae': 'banner added successfilly'}
            return JsonResponse(response_data, status=200)
    
    def Delete(self, request):
        data = request.data
        if 'ids' in data and len(data['ids']) > 0:        
            response_data = {'messgae': 'select banner'}
            return JsonResponse(response_data, status=422)
        method = data['method'] if 'method' in data else 1
        if method == 1:
            for ids in data['ids']:
                db.banner.delete_one(
                    {"_id": ObjectId(ids)})
                response_data = {'messgae': 'banner stat deleting successfilly'}
                return JsonResponse(response_data, status=200)
        else:
            for ids in data['ids']:
                db.banner.update_one(
                    {"_id": ObjectId(ids)} ,
                    {"status": 3}
                    )
                response_data = {'messgae': 'banner stat deleting successfilly'}
                return JsonResponse(response_data, status=200)
            


    ''' sound '''
    
    ''' gift '''



          