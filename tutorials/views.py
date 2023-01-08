from django.shortcuts import render
# render:是一個函數，用於渲染模板文件，並返回響應數據。

from django.http.response import JsonResponse
# JsonResponse:是一個類，用於將數據轉換為JSON格式的響應數據。
from rest_framework.parsers import JSONParser 
# JSONParser:是一個解析器類，用於解析JSON格式的請求數據。
from rest_framework import status
# status:是一個模塊，用於定義HTTP狀態碼。
 
from tutorials.models import Tutorial
# Tutorial:是一個模型類，用於定義數據庫中的表結構。
from tutorials.serializers import TutorialSerializer
# TutorialSerializer:是一個序列化器類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。
from rest_framework.decorators import api_view
# api_view:是一個函式裝飾器，用於將函式轉換為視圖，並將函式的輸入和輸出轉換為REST框架請求和響應。


@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    
    if request.method == 'GET':
        # requst.method: 是一個屬性，用於獲取請求的方法。
        tutorials = Tutorial.objects.all()
        # Tutorial.objects.all(): 是一個方法，用於獲取數據庫中的所有記錄。
        
        title = request.GET.get('title', None)
        # request.GET.get(): 是一個方法，用於獲取請求中的參數。 title: 是參數的名稱。 None: 是參數的默認值。
        if title is not None:
            # 如果title不為None，則進行過濾。
            tutorials = tutorials.filter(title__icontains=title)
            # tutorials.filter(): 是一個方法，用於過濾數據庫中的記錄。 title__icontains: 是過濾條件，表示title中包含title參數的值。
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        # TutorialSerializer(): 是一個類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。tutorial: 是要轉換的模型實例。 many=True: 表示要轉換的模型實例是多個。
        return JsonResponse(tutorials_serializer.data, safe=False)
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 tutorials_serializer.data: 是要轉換的數據。 safe=False: 表示要轉換的數據是多個。
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        # 如果請求的方法是POST，則進行新增操作。
        tutorial_data = JSONParser().parse(request)
        # JSONParser().parse(): 是一個方法，用於解析JSON格式的請求數據。 request: 是請求數據。
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        # TutorialSerializer(): 是一個類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。 data=tutorial_data: 是要轉換的數據。
        if tutorial_serializer.is_valid():
            # tutorial_serializer.is_valid(): 是一個方法，用於驗證數據是否合法。
            tutorial_serializer.save()
            # tutorial_serializer.save(): 是一個方法，用於保存數據。
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
            # status.HTTP_201_CREATED: 是一個常量，用於表示201狀態碼。201_CREATED: 表示新增成功。
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # status.HTTP_400_BAD_REQUEST: 是一個常量，用於表示400狀態碼。400_BAD_REQUEST: 表示請求數據不合法。
    
    elif request.method == 'DELETE':
        # 如果請求的方法是DELETE，則進行刪除操作。
        count = Tutorial.objects.all().delete()
        # Tutorial.objects.all().delete(): 是一個方法，用於刪除數據庫中的所有記錄。
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 count[0]: 是要轉換的數據。 status.HTTP_204_NO_CONTENT: 是一個常量，用於表示204狀態碼。204_NO_CONTENT: 表示刪除成功。
        # format(): 是一個方法，用於格式化字符串。
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # tutorial_detail(): 是一個函數，用於處理請求。request: 是請求數據。pk: 是要操作的記錄的主鍵。
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
        # Tutorial.objects.get(): 是一個方法，用於查詢數據庫中的記錄。pk=pk: 是要查詢的記錄的主鍵。
    except Tutorial.DoesNotExist: 
        # Tutorial.DoesNotExist: 是一個異常，用於表示查詢的記錄不存在。
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        # status.HTTP_404_NOT_FOUND: 是一個常量，用於表示404狀態碼。404_NOT_FOUND: 表示查詢的記錄不存在。
 
    if request.method == 'GET': 
        # 如果請求的方法是GET，則進行查詢操作。
        tutorial_serializer = TutorialSerializer(tutorial)
        # TutorialSerializer(): 是一個類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。 tutorial: 是要轉換的數據。
        return JsonResponse(tutorial_serializer.data) 
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 tutorial_serializer.data: 是要轉換的數據。
 
    elif request.method == 'PUT': 

        tutorial_data = JSONParser().parse(request) 
        # JSONParser(): 是一個類，用於將JSON格式的數據轉換為Python數據類型。 tutorial_data: 是要轉換的數據。 request: 是請求數據。
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        # TutorialSerializer(): 是一個類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。 tutorial: 是要轉換的數據。 data=tutorial_data: 是要轉換的數據。
        if tutorial_serializer.is_valid(): 
            # tutorial_serializer.is_valid(): 是一個方法，用於判斷數據是否有效。is_valid(): 表示數據有效。
            tutorial_serializer.save() 
            # tutorial_serializer.save(): 是一個方法，用於保存數據。save(): 表示保存數據。
            return JsonResponse(tutorial_serializer.data) 
            # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 tutorial_serializer.data: 是要轉換的數據。
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 tutorial_serializer.errors: 是要轉換的數據。 status.HTTP_400_BAD_REQUEST: 是一個常量，用於表示400狀態碼。400_BAD_REQUEST: 表示數據無效。
 
    elif request.method == 'DELETE': 
        # 如果請求的方法是DELETE，則進行刪除操作。
        tutorial.delete() 
        # tutorial.delete(): 是一個方法，用於刪除數據。delete(): 表示刪除數據。
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 {'message': 'Tutorial was deleted successfully!'}: 是要轉換的數據。 status.HTTP_204_NO_CONTENT: 是一個常量，用於表示204狀態碼。204_NO_CONTENT: 表示刪除數據成功。
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    # api_view(): 是一個裝飾器，用於將函數轉換為API視圖。 ['GET']: 表示只接受GET請求。
    # tutorial_list_published(): 是一個函數，用於查詢已發布的教程。
    tutorials = Tutorial.objects.filter(published=True)
    # Tutorial.objects.filter(): 是一個方法，用於查詢符合條件的數據。 published=True: 表示查詢已發布的教程。
        
    if request.method == 'GET': 
        # 如果請求的方法是GET，則進行查詢操作。
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        # TutorialSerializer(): 是一個類，用於將模型實例轉換為JSON格式的數據，或者將JSON格式的數據轉換為模型實例。 tutorials: 是要轉換的數據。 many=True: 表示轉換多個數據。
        return JsonResponse(tutorials_serializer.data, safe=False)
        # JsonResponse(): 是一個類，用於將數據轉換為JSON格式的響應數據。 tutorials_serializer.data: 是要轉換的數據。 safe=False: 表示數據不安全。
    
