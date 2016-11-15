from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect

perms = (
            # ('watch_fileable',u'可以查看文件'),
            ('del_fileable',u'可以删除文件'),
            ('download_fileable',u'可以下载文件'),
            ('upload_fileable',u'可以上传文件'),
        )

perm_dic = {
            # 'watch_fileable':[],
            'del_fileable':['index','POST',['RemoveImg',]],
            'download_fileable':['index','GET',[]],
            'upload_fileable':['index','FILES',['f1',]],
        }



def perm_check(*args,**kwargs):
     request = args[0]
     url_resovle_obj = resolve(request.path_info)
     current_url_namespace = url_resovle_obj.url_name
     matched_flag = False # find matched perm item
     matched_perm_key = None

     print(request.user.has_perm('sharefile.del_fileable'))
     print(request.user.has_perm('sharefile.download_fileable'))
     print(request.user.has_perm('sharefile.upload_fileable'))
     if current_url_namespace is not None:#if didn't set the url namespace, permission doesn't work
         for perm_key in perm_dic:
             perm_val = perm_dic[perm_key]
             if len(perm_val) == 3:#otherwise invalid perm data format
                 url_namespace,request_method,request_args = perm_val
                 if url_namespace == current_url_namespace: #matched the url
                     if request.method == request_method:#matched request method
                         if not request_args:#if empty , pass
                             matched_flag = True
                             matched_perm_key = perm_key
                             break #no need looking for  other perms
                         else:
                             for request_arg in request_args: #might has many args
                                 request_method_func = getattr(request,request_method) #get or post mostly
                                 if request_method_func.get(request_arg) is not None:
                                     matched_flag = True # the arg in set in perm item must be provided in request data
                                 else:
                                     matched_flag = False
                                     break #no need go further
                             if matched_flag == True: # means passed permission check ,no need check others
                                 matched_perm_key = perm_key
                                 break
                     else:
                         if not request_args:#if empty , pass
                             matched_flag = True
                             matched_perm_key = perm_key

                             break #no need looking for  other perms
                         else:

                             for request_arg in request_args: #might has many args
                                 request_method_func = request.FILES
                                 if request_method_func.get(request_arg) is not None:
                                     matched_flag = True # the arg in set in perm item must be provided in request data
                                 else:
                                     matched_flag = False
                                     break #no need go further
                             if matched_flag == True: # means passed permission check ,no need check others
                                 matched_perm_key = perm_key
                                 break
     else:#permission doesn't work
         return False

     if matched_flag == True:
         #pass permission check
         perm_str = "sharefile.%s" %(matched_perm_key)

         if request.user.has_perm(perm_str):
             return True
         else:
             return False



def check_permission(func):
     def wrapper(*args,**kwargs):
         if  perm_check(*args,**kwargs) is not True:
             return render(args[0],'app/error403.html')
         return func(*args,**kwargs)
     return wrapper