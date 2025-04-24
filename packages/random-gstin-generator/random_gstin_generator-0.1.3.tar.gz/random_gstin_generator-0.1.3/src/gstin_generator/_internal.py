import random
import string

state_codes = {
    "01": "Jammu & Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman and Diu",
    "26": "Dadra and Nagar Haveli",
    "27": "Maharashtra",
    "28": "Andhra Pradesh (Before 2014)",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar Islands",
    "36": "Telangana",
    "37": "Andhra Pradesh (New)"
}

def generate_gstin(num_gstins: int = 1) -> list[str]:
    def generate_pan():
        first_letter = random.choice(['A', 'B', 'C', 'F', 'G', 'H', 'L', 'J', 'P', 'T'])
        letters = ''.join(random.choices(string.ascii_uppercase, k=4))
        digits = ''.join(random.choices(string.digits, k=4))
        last_letter = random.choice(string.ascii_uppercase)
        return f"{first_letter}{letters}{digits}{last_letter}"
    
    def calculate_checksum(gst):
        l = [int(c) if c.isdigit() else ord(c) - 55 for c in gst]
        l = [val * (ind % 2 + 1) for ind, val in enumerate(l)]
        l = [(x // 36) + x % 36 for x in l]
        csum = (36 - sum(l) % 36)
        return str(csum) if csum < 10 else chr(csum + 55)

    def generate_random_entity_code():
        return str(random.randint(0, 9)) if random.choice([True, False]) else random.choice(string.ascii_uppercase)

    def generate_valid_gstin():
        state_code = random.choice(list(state_codes.keys()))
        pan = generate_pan()
        entity_code = generate_random_entity_code()
        gstin_without_checksum = f"{state_code}{pan}{entity_code}Z"
        checksum = calculate_checksum(gstin_without_checksum)
        return f"{gstin_without_checksum}{checksum}"

    return [generate_valid_gstin() for _ in range(num_gstins)]