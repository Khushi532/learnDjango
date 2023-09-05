from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # This decorator allows POST requests without CSRF tokens (for simplicity)
def cal_sd(request):
    # if request.method == 'POST':
    #     try:
    #         data = json.loads(request.body.decode('utf-8'))
    #         values = data.get('values', [])
    #         sub_group_size = data.get('sub_group_size', 1)

    #         # Your calculation function
    #         def calculate_overall_sd(values, sub_group_size):
    #             mean = 0
    #             total = 0
    #             mean_total = 0
    #             counter = 0

    #             for i in range(0, len(values), sub_group_size):
    #                 if i + sub_group_size > len(values):
    #                     break
    #                 else:
    #                     for j in range(i, i + sub_group_size):
    #                         total += float(values[j])
    #                         counter += 1

    #             mean = total / counter

    #             for i in range(0, len(values), sub_group_size):
    #                 if i + sub_group_size > len(values):
    #                     break
    #                 else:
    #                     for j in range(i, i + sub_group_size):
    #                         mean_total += (mean - float(values[j])) ** 2

    #             return (mean_total / (counter - 1)) ** 0.5

    #         result = calculate_overall_sd(values, sub_group_size)
    #         return JsonResponse({'result': result})

    #     except Exception as e:
    #         return JsonResponse({'error': str(e)})

    return render(request,'cal_sd.html')
