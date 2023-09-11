from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from .data import data 
import math

#================================================================================
# Calculate sd
#================================================================================
def calculate_overall_sd(values, sub_group_size):
    mean = 0
    total = 0
    mean_total = 0
    counter = 0

    for i in range(0, len(values), sub_group_size):
        if i + sub_group_size > len(values):
            break
        else:
            for j in range(i, i + sub_group_size):
                total += float(values[j])
                counter += 1

    mean = total / counter

    for i in range(0, len(values), sub_group_size):
        if i + sub_group_size > len(values):
            break
        else:
            for j in range(i, i + sub_group_size):
                mean_total += (mean - float(values[j])) ** 2

    return (mean_total / (counter - 1)) ** 0.5


def calculate_cp(upper_limit, lower_limit, values, sub_group_size):
    def calculate_average(data):
        total = 0
        counter = 0
        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            for j in range(i, i + sub_group_size):
                total += float(data[j])
                counter += 1
        return total / counter

    def calculate_range(data, size):
        range_values = []
        if size == 1:
            for i in range(1, len(data)):
                range_values.append(abs(float(data[i]) - float(data[i - 1])))
        else:
            max_value = float(data[0])
            min_value = float(data[0])
            for i in range(0, len(data), size):
                if i + size > len(data):
                    break
                else:
                    max_value = float(data[i])
                    min_value = float(data[i])
                    for j in range(i, i + size):
                        current_value = float(data[j])
                        if max_value < current_value:
                            max_value = current_value
                        if min_value > current_value:
                            min_value = current_value
                    range_values.append(max_value - min_value)
        return range_values

    if upper_limit is None or lower_limit is None or str(upper_limit) == 'nan' or str(lower_limit) == 'nan':
        return str(float('nan'))
    else:
        range_data = calculate_range(values, sub_group_size)
        average_range = calculate_average(range_data)
        D2 = [1.128, 1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.97, 3.078, 3.173, 3.258, 3.336, 3.407, 3.472]
        potential_SD = average_range / D2[sub_group_size - 1]
        return str((upper_limit - lower_limit) / (6 * potential_SD))


#================================================================================
# Calculate Cpk
#================================================================================
def calculate_cpk(values, sub_group_size, upper_limit=None, lower_limit=None):
    def calculate_average(data):
        total = 0
        counter = 0
        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            for j in range(i, i + sub_group_size):
                total += float(data[j])
                counter += 1
        return total / counter

    def calculate_range(data, size):
        range_values = []
        if size == 1:
            for i in range(1, len(data)):
                range_values.append(abs(float(data[i]) - float(data[i - 1])))
        else:
            max_value = float(data[0])
            min_value = float(data[0])
            for i in range(0, len(data), size):
                if i + size > len(data):
                    break
                else:
                    max_value = float(data[i])
                    min_value = float(data[i])
                    for j in range(i, i + size):
                        current_value = float(data[j])
                        if max_value < current_value:
                            max_value = current_value
                        if min_value > current_value:
                            min_value = current_value
                    range_values.append(max_value - min_value)
        return range_values

    def calculate_potential_sd(data):
        range_data = calculate_range(data, sub_group_size)
        average = calculate_average(range_data)
        D2 = [1.128, 1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.97, 3.078, 3.173, 3.258, 3.336, 3.407, 3.472]
        return average / D2[sub_group_size - 1]

    def calculate_cp_upper(upper_limit, data):
        if upper_limit is None or str(upper_limit) == 'nan':
            return str(float('nan'))
        else:
            potential_SD = calculate_potential_sd(data)
            average = calculate_average(data)
            return str((upper_limit - average) / (3 * potential_SD))

    def calculate_cp_lower(lower_limit, data):
        if lower_limit is None or str(lower_limit) == 'nan':
            return str(float('nan'))
        else:
            potential_SD = calculate_potential_sd(data)
            average = calculate_average(data)
            return str((average - lower_limit) / (3 * potential_SD))

    def calculate_cpk(CpUpper, CpLower):
        if CpUpper is None or CpLower is None or str(CpUpper) == 'nan' or str(CpLower) == 'nan':
            return str(float('nan'))
        else:
            return str(min(CpUpper, CpLower))

    CpUpper = calculate_cp_upper(upper_limit, values)
    CpLower = calculate_cp_lower(lower_limit, values)
    return calculate_cpk(CpUpper, CpLower)


#================================================================================
# Calculate pp
#================================================================================
def calculate_pp(upper_limit, lower_limit, values, sub_group_size):
    def calculate_overall_sd(data):
        mean = 0
        total = 0
        mean_total = 0
        counter = 0
        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            else:
                for j in range(i, i + sub_group_size):
                    total += float(data[j])
                    counter += 1

        mean = total / counter

        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            else:
                for j in range(i, i + sub_group_size):
                    mean_total += (mean - float(data[j])) ** 2

        return (mean_total / (counter - 1)) ** 0.5

    if upper_limit is None or lower_limit is None or str(upper_limit) == 'nan' or str(lower_limit) == 'nan':
        return str(float('nan'))
    else:
        overall_SD = calculate_overall_sd(values)
        return str((upper_limit - lower_limit) / (6 * overall_SD))

#================================================================================
# Calculate ppk
#================================================================================

def calculate_ppk(upper_limit, lower_limit, data, sub_group_size):
    def calculate_overall_sd(data, sub_group_size):
        mean = 0
        total = 0
        mean_total = 0
        counter = 0
        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            else:
                for j in range(i, i + sub_group_size):
                    total += float(data[j])
                    counter += 1

        mean = total / counter

        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            else:
                for j in range(i, i + sub_group_size):
                    mean_total += (mean - float(data[j])) ** 2

        return math.sqrt(mean_total / (counter - 1))

    def calculate_average(data, sub_group_size):
        total = 0
        counter = 0
        for i in range(0, len(data), sub_group_size):
            if i + sub_group_size > len(data):
                break
            else:
                for j in range(i, i + sub_group_size):
                    total += float(data[j])
                    counter += 1

        return total / counter

    def calculate_pp_upper(upper_limit, data, sub_group_size):
        if upper_limit is None or math.isnan(upper_limit):
            return float('nan')
        else:
            overall_SD = calculate_overall_sd(data, sub_group_size)
            average = calculate_average(data, sub_group_size)
            return (upper_limit - average) / (3 * overall_SD)

    def calculate_pp_lower(lower_limit, data, sub_group_size):
        if lower_limit is None or math.isnan(lower_limit):
            return float('nan')
        else:
            overall_SD = calculate_overall_sd(data, sub_group_size)
            average = calculate_average(data, sub_group_size)
            return (average - lower_limit) / (3 * overall_SD)

    def calculate_ppk(upper_limit, lower_limit, data, sub_group_size):
        Pp_upper = float('nan')
        Pp_lower = float('nan')

        temp_var = calculate_pp_upper(upper_limit, data, sub_group_size)
        if not math.isnan(temp_var):
            Pp_upper = temp_var

        temp_var = calculate_pp_lower(lower_limit, data, sub_group_size)
        if not math.isnan(temp_var):
            Pp_lower = temp_var

        return min(Pp_upper, Pp_lower)

    return calculate_ppk(upper_limit, lower_limit, data, sub_group_size)


#================================================================================
# Calculate ppm
#================================================================================

def calculate_ppm(values, sub_group_size, usl, lsl):
    def calculate_overall_sd(values, sub_group_size):
        mean = 0
        total = 0
        mean_total = 0
        counter = 0

        for i in range(0, len(values), sub_group_size):
            if i + sub_group_size > len(values):
                break
            else:
                for j in range(i, i + sub_group_size):
                    total += float(values[j])
                    counter += 1

        mean = total / counter

        for i in range(0, len(values), sub_group_size):
            if i + sub_group_size > len(values):
                break
            else:
                for j in range(i, i + sub_group_size):
                    mean_total += (mean - float(values[j])) ** 2

        return math.sqrt(mean_total / (counter - 1))

    def calculate_average(values, sub_group_size):
        total = 0
        counter = 0

        for i in range(0, len(values), sub_group_size):
            if i + sub_group_size > len(values):
                break
            else:
                for j in range(i, i + sub_group_size):
                    total += float(values[j])
                    counter += 1

        return total / counter

    def prob_norm(z):
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    ret_array = [None] * 3
    a_sigma = calculate_overall_sd(values, sub_group_size)
    a_xbar = calculate_average(values, sub_group_size)

    z_usl = None
    z_lsl = None

    if usl is not None:
        z_usl = (usl - a_xbar) / a_sigma

    if lsl is not None:
        z_lsl = (lsl - a_xbar) / a_sigma

    lower_ppm = None
    upper_ppm = None
    total_ppm = None

    if z_lsl is not None:
        lower_ppm = prob_norm(z_lsl)

    if z_usl is not None:
        upper_ppm = 1 - prob_norm(z_usl)

    if upper_ppm is not None:
        total_ppm = upper_ppm
        ret_array[1] = f"{upper_ppm * 1000000:.3f}"
        ret_array[2] = f"{total_ppm * 1000000:.3f}"
        if lower_ppm is not None:
            total_ppm = lower_ppm + upper_ppm
            ret_array[0] = f"{lower_ppm * 1000000:.3f}"  
            ret_array[1] = f"{upper_ppm * 1000000:.3f}"  
            ret_array[2] = f"{total_ppm * 1000000:.3f}"  
        else:
            ret_array[0] = "NaN"
    else:
        if lower_ppm is not None:
            total_ppm = lower_ppm
            ret_array[0] = f"{lower_ppm * 1000000:.3f}"  # Format to 3 decimal places
            ret_array[2] = f"{total_ppm * 1000000:.3f}"  # Format to 3 decimal places
            ret_array[1] = "NaN"

    return ret_array

#================================================================================
# Calculate-combined
#================================================================================

def calculate(request):

    if request.method == 'POST':
        values = request.POST['values'].split(',')
        sub_group_size = int(request.POST['sub_group_size'])
        
        # Handle upper_limit input
        upper_limit_str = request.POST.get('upper_limit', '')
        if upper_limit_str.strip():
            upper_limit = float(upper_limit_str)
        else:
            upper_limit = 'N/A'

        # Handle lower_limit input
        lower_limit_str = request.POST.get('lower_limit', '')
        if lower_limit_str.strip():
            lower_limit = float(lower_limit_str)
        else:
            lower_limit = 'N/A'

        sd_result = calculate_overall_sd(values, sub_group_size)

        upper_limit_str = request.POST['upper_limit']
        upper_limit = int(upper_limit_str) if upper_limit_str.strip() else 'NA'
        lower_limit_str = request.POST['lower_limit']
        lower_limit = int(lower_limit_str) if lower_limit_str.strip() else 'NA'

        # Calculate CP
        cp_result = calculate_cp(upper_limit, lower_limit, values, sub_group_size)

        # Calculate Cpk
        cpk_result = calculate_cpk(values, sub_group_size,upper_limit, lower_limit)

        #Calculate pp
        pp_result = calculate_pp(upper_limit, lower_limit, values, sub_group_size)

        #Calculate ppk
        ppk_result = calculate_ppk(upper_limit, lower_limit, values, sub_group_size)

        #Calculate ppm
        ppm_result = calculate_ppm(values,sub_group_size,upper_limit,lower_limit)


        new_data = {
            'values': ','.join(values),
            'sub_group_size': sub_group_size,
            'sd': sd_result,
            'upper_limit': upper_limit,
            'lower_limit': lower_limit,
            'cp': cp_result,
            'cpk': cpk_result,
            'pp': pp_result,
            'ppk': ppk_result,
            'ppm':ppm_result
        }

        data.append(new_data)
    return render(request, 'cal_sd.html', {'data': data})