
# Create your views here.
from django.shortcuts import render
from . recommendator import recommend, load_data, get_course_by_id,get_popular_courses
from django.shortcuts import redirect


load_data()

def home(request):
    query = ""
    results = []
    header_text = "" 
    
    if request.method == 'POST':
        query = request.POST.get('search_query', '')
        
    
        if query.strip(): 
            results = recommend(query)
            header_text = f'Top Results for "{query}"'
        else:
            
            results = get_popular_courses(N=6)
            header_text = "Trending Courses (Most Popular)"
            query = "" 
            
    else:
        results = get_popular_courses(N=6)
        header_text = "Trending Courses (Most Popular)"

    return render(request, 'home.html', {
        'results': results, 
        'query': query,
        'header_text': header_text
    })
  

def course_detail(request, course_id):
    course = get_course_by_id(course_id)
    
    if course is None:

        return redirect('index')
    
    return render(request, 'course_detail.html', {'course': course})