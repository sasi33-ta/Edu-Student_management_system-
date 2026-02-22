def theme_processor(request):
    return {'current_theme': request.COOKIES.get('theme', 'dark')}
