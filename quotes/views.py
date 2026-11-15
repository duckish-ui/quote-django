from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Quote
import random
import json


def quote_to_dict(quote):
    return {'id': quote.id, 'text': quote.text, 'author': quote.author}


def parse_body(request):
    try:
        return json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return None


# ============ TEMPLATE VIEWS (return HTML) ============

# TODO 7: home view - random quote
def home(request):
    quotes = list(Quote.objects.all())
    quote = random.choice(quotes) if quotes else None
    return render(request, 'quotes/home.html', {'quote': quote})


# TODO 8: all_quotes view
def all_quotes(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/all_quotes.html', {'quotes': quotes})


# ============ API VIEWS (return JSON) ============

# TODO 9: random_quote_api
def random_quote_api(request):
    quotes = list(Quote.objects.all())
    if not quotes:
        return JsonResponse({'error': 'No quotes available'}, status=404)
    return JsonResponse(quote_to_dict(random.choice(quotes)))


@csrf_exempt  # Allows POST/PUT/DELETE without CSRF token
def quotes_api(request):
    # TODO 10: GET all quotes / POST a new quote
    if request.method == 'GET':
        return JsonResponse([quote_to_dict(q) for q in Quote.objects.all()], safe=False)

    if request.method == 'POST':
        data = parse_body(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        text = data.get('text')
        author = data.get('author')
        if not text or not author:
            return JsonResponse({'error': "Both 'text' and 'author' are required"}, status=400)
        quote = Quote.objects.create(text=text, author=author)
        return JsonResponse(quote_to_dict(quote), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def quote_detail_api(request, id):
    # TODO 11: GET / PUT / DELETE a single quote
    try:
        quote = Quote.objects.get(id=id)
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(quote_to_dict(quote))

    if request.method == 'PUT':
        data = parse_body(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if 'text' in data:
            quote.text = data['text']
        if 'author' in data:
            quote.author = data['author']
        quote.save()
        return JsonResponse(quote_to_dict(quote))

    if request.method == 'DELETE':
        quote.delete()
        return JsonResponse({'message': f'Quote {id} deleted successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)
