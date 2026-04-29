def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            result.append(left_half[i])
            i += 1
        else:
            result.append(right_half[j])
            j += 1

    result.extend(left_half[i:])
    result.extend(right_half[j:])
    return result






# =================================================================
# 2. BREADTH-FIRST SEARCH (BFS)
# =================================================================
def find_path(graph, start, end):
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == end:
            return path
        
        if node not in visited:
            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(node)
            
    return None # Path not found







# =================================================================
# 3. SIEVE OF ERATOSTHENES
# =================================================================
def get_primes(limit):
    if limit < 2:
        return []
    
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    
    for p in range(2, int(limit**0.5) + 1):
        if primes[p]:
            for i in range(p * p, limit + 1, p):
                primes[i] = False
                
    result = []
    for num, is_prime in enumerate(primes):
        if is_prime:
            result.append(num)
            
    return result










# =================================================================
# 4. PASSWORD COMPLEXITY VALIDATOR
def validate_password(password, min_len=8):
    if len(password) < min_len:
        return False, "Too short"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    special = "!@$%^&*"
    has_spec = any(c in special for c in password)

    if not (has_upper and has_lower):
        return False, "Case mismatch"
    if not has_digit:
        return False, "No numbers"
    if not has_spec:
        return False, "No special chars"
        
    return True, "Strong password"











# 5. CUSTOM CSV LINE PARSER
def parse_csv_line(line, delimiter=",", quote='"'):
    results = []
    current = ""
    in_quotes = False

    for char in line:
        if char == quote:
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            results.append(current.strip())
            current = ""
        else:
            current += char
            
    results.append(current.strip())
    final = [res for res in results if len(res) > 0]
    
    return final if len(final) > 0 else None









# =================================================================
# 6. API RESPONSE FORMATTER
# =================================================================
def format_api_response(raw_data, version=1.0):
    output = {
        "metadata": {"version": version, 
                    "status": "success"},
        "payload": []
    }

    for item in raw_data:
        processed = {
            "uid": item.get("id", 0),
            "label": item.get("name", "Unknown").upper(),
            "is_valid": item.get("score", 0) > 50,
            "tags": item.get("categories", [])
        }
        output["payload"].append(processed)

    if len(output["payload"]) == 0:
        output["metadata"]["status"] = "empty"
        
    return output







# =================================================================
# 7. SHOPPING CART MANAGER
# =================================================================
class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self.discount = 0.0

    def add_item(self, name, price, qty=1):
        if price <= 0: return False
        self.items.append({"name": name, "price": price, 
                           "qty": qty})
        return True

    def get_total(self):
        total = sum(i["price"] * i["qty"] 
                            for i in self.items)
        if total > 1000:
            self.discount = 0.1
        return total * (1 - self.discount)

    def clear(self):
        self.items = []
        self.discount = 0.0





с =ShoppingCart()# =================================================================
# 8. FILE LOGGER SYSTEM
# =================================================================
class FileLogger:
    def __init__(self, filename, level="INFO"):
        self.file = filename
        self.level = level
        self.logs_count = 0

    def log(self, message, priority="INFO"):
        fmt = f"[{priority}] {message}"
        try:
            with open(self.file, "a") as f:
                f.write(fmt + "\n")
            self.logs_count += 1
            return True
        except Exception as e:
            print(f"Failed to log: {e}")
            return False

    def get_stats(self):
        return f"File: {self.file}, Res: {self.logs_count}"





с =FileLogger()


# =================================================================
# 9. RECTANGLE GEOMETRY CLASS
# =================================================================
import math

class Rectangle:
    def __init__(self, width, height, color="red"):
        self.w = width
        self.h = height
        self.color = color

    def area(self): return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

    def scale(self, factor):
        if factor > 0:
            self.w *= factor
            self.h *= factor
            return True
        return False

    def info(self):
        return f"{self.color} rect: {self.w}x{self.h}"




с =Rectangle()
# =================================================================
# 10. TEXT SANITIZATION UTILITY
# =================================================================
def sanitize_text(input_str, allow_numbers=True):
    forbidden = ["$", "&", ";", "<", ">", "/", "\\"]
    result = ""

    for char in input_str:
        if char in forbidden:
            continue
        if char.isdigit() and not allow_numbers:
            continue
        result += char

    cleaned = result.strip()
    if len(cleaned) > 50:
        return cleaned[:47] + "..."
    
    return cleaned if cleaned else "n/a"











# =================================================================
# 11. SAMPLE STATISTICS CALCULATOR
# =================================================================
def get_statistics(numbers):
    if not numbers:
        return {"mean": 0, "max": 0, "min": 0}
    
    total = sum(numbers)
    count = len(numbers)
    mean = total / count
    
    sorted_nums = sorted(numbers)
    mid = count // 2
    if count % 2 == 0:
        median = (sorted_nums[mid - 1] + 
                            sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]
        
    return {
        "mean": round(mean, 2),
        "median": median,
        "count": count
    }






# =================================================================
# 12. HTTP FETCH WITH RETRY MOCK
# =================================================================
def fetch_with_retry(url, retries=3, timeout=5):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Connecting to {url}, try {attempt + 1}")
            if "error" in url:
                raise ConnectionError("Server Down")
            return {"code": 200, "data": "Success"}
        except Exception as err:
            print(f"Error: {err}")
            attempt += 1
            
    return {"code": 500, "data": None}














# =================================================================
# 13. CURRENCY CONVERTER LOGIC
# =================================================================
def convert_currency(amount, rate, fee_percent=2.5):
    if amount <= 0:
        return 0.0
    
    raw_convert = amount * rate
    fee_amount = (raw_convert * fee_percent) / 100
    
    final_amount = round(raw_convert - fee_amount, 2)
    
    if final_amount < 0.01:
        print("Warning: Amount too small")
        return 0.0
        
    return final_amount













# =================================================================
# 14. UNIQUE ID GENERATOR
# =================================================================
import random
import string

def generate_id(length=12, use_special=False):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@*-_"
        
    unique_id = ""
    for _ in range(length):
        char = random.choice(chars)
        unique_id += char
        
    prefix = "ID_"
    if unique_id.startswith("0"):
        unique_id = "X" + unique_id[1:]
        
    return prefix + unique_id









# =================================================================
# 15. SERVER LOG ANALYZER
# =================================================================
def analyze_server_logs(logs):
    error_count = 0
    critical_ips = set()
    
    for entry in logs:
        parts = entry.split(" - ")
        if len(parts) < 3:
            continue
            
        status = parts[1]
        ip = parts[2]
        
        if status == "ERROR":
            error_count += 1
        elif status == "CRITICAL":
            critical_ips.add(ip)
            
    return {
        "total_errors": error_count,
        "unique_critical_ips": list(critical_ips)
    }






# =================================================================
# 16. LIST DUPLICATE FINDER
# =================================================================
def find_duplicates(items):
    seen = {}
    dupes = []
    
    for val in items:
        if val in seen:
            seen[val] += 1
        else:
            seen[val] = 1
            
    for key, count in seen.items():
        if count > 1:
            dupes.append(key)
            
    dupes.sort()
    return dupes if len(dupes) > 0 else []











# =================================================================
# 17. MATRIX ADDITION CALCULATOR
# =================================================================
def add_matrices(mat_a, mat_b):
    if len(mat_a) != len(mat_b) 
                or len(mat_a[0]) != len(mat_b[0]):
        return None
        
    rows = len(mat_a)
    cols = len(mat_a[0])
    result = []
    
    for r in range(rows):
        new_row = []
        for c in range(cols):
            sum_val = mat_a[r][c] + mat_b[r][c]
            new_row.append(sum_val)
        result.append(new_row)
        
    return result










# =================================================================
# 18. SIMPLE LRU CACHE MOCK
# =================================================================
class SimpleCache:
    def __init__(self, limit=5):
        self.store = {}
        self.order = []
        self.limit = limit

    def set(self, key, value):
        if key in self.store:
            self.order.remove(key)
        elif len(self.order) >= self.limit:
            oldest = self.order.pop(0)
            del self.store[oldest]
            
        self.store[key] = value
        self.order.append(key)

    def get(self, key):
        return self.store.get(key, None)








c = SimpleCache()
# =================================================================
# 19. TIME DURATION FORMATTER
# =================================================================
def format_duration(seconds):
    if seconds < 0:
        return "00:00:00"
        
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    h_str = str(hours).zfill(2)
    m_str = str(minutes).zfill(2)
    s_str = str(secs).zfill(2)
    
    res = f"{h_str}:{m_str}:{s_str}"
    return res if hours < 100 else "99:59:59"













# =================================================================
# 20. TASK QUEUE PROCESSOR
# =================================================================
def process_tasks(queue):
    completed = 0
    failed = 0
    
    while len(queue) > 0:
        current_task = queue.pop(0)
        task_id = current_task.get("id")
        
        if current_task.get("priority") == "high":
            status = True 
        else:
            # Random simulation for testing
            status = (task_id % 2 == 0)
            
        if status:
            completed += 1
        else:
            failed += 1
            
    return completed, failed



















# def quick_sort(arr):
#     if len(arr) <= 1:
#         return arr

#     pivot = arr[len(arr) // 2]
    
#     left = [x for x in arr if x < pivot]
#     middle = [x for x in arr if x == pivot]
#     right = [x for x in arr if x > pivot]

    
#     return quick_sort(left) + middle + quick_sort(right)

# data_set = [3, 6, 8, 10, 1, 2, 1]



# import math

# def square(x):
#     return x * x

# def process():
#     values = [1, 2, 3]

#     for v in values:
#         res = square(v)
#         print(res)

#     return True

# flag = process()


# value = 4

# def calc(n):
#     total = 0
#     for i in range(n):
#         total = total + i
#     return total

# result = calc(value)


# def sum(a, b):
#     result = a + b
#     return result

# x = 4
# y = 6

# res = sum(x, y)




# import math

# def cube(a):
#     return a * a * a

# def run():
#     data = [2, 3, 4]

#     for item in data:
#         result = cube(item)
#         print(result)

#     return False

# status = run()


# count = 3

# def compute(k):
#     acc = 1
#     for j in range(k):
#         acc = acc * (j + 1)
#     return acc

# final = compute(count)


# def multiply(a, b):
#     output = a * b
#     return output

# m = 3
# n = 5

# res = multiply(m, n)

