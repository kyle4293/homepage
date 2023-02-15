from django.shortcuts import render, get_object_or_404

def portfolio(request):
    return render(request, 'portfolio/portfolio_home.html')