from django.shortcuts import redirect


def redirect_to_main(request):
    return redirect('post:post_list')
