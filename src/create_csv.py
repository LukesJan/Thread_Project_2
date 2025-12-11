import csv
import random
filename = "large_data.csv"
num_records = 1000000
ERROR_RATE = 0.01

names = [
    "Printer", "Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Router", "Headphones", "Camera",
    "Smartwatch", "TV", "Speaker", "Fridge", "Microwave", "Oven", "Blender", "Vacuum", "Air Conditioner", "Dishwasher",
    "Coffee Maker", "Toaster", "Electric Kettle", "Fan", "Heater", "Projector", "Scanner", "External Hard Drive", "USB Drive", "Memory Card",
    "Smart Light", "Smart Plug", "Smart Thermostat", "Gaming Console", "VR Headset", "Drone", "Action Camera", "Fitness Tracker", "Electric Scooter", "Electric Bike",
    "Water Filter", "Juicer", "Slow Cooker", "Rice Cooker", "Bread Maker", "Ice Maker", "Pressure Cooker", "Food Processor", "Mixer", "Grill",
    "Hair Dryer", "Hair Straightener", "Shaver", "Electric Toothbrush", "Iron", "Sewing Machine", "Camera Lens", "Tripod", "Microphone", "Webcam",
    "Router Modem", "Network Switch", "NAS Drive", "Server Rack", "Laptop Bag", "Phone Case", "Tablet Case", "Screen Protector", "Power Bank", "Bluetooth Adapter",
    "Graphics Card", "CPU", "Motherboard", "RAM", "Power Supply", "Cooling Fan", "Monitor Stand", "Desk Lamp", "Office Chair", "Desk",
    "Notebook", "Pen", "Pencil", "Marker", "Stapler", "Paper Shredder", "Whiteboard", "Bulletin Board", "Planner", "Calculator",
    "Board Game", "Puzzle", "Toy Car", "Doll", "Action Figure", "Building Blocks", "Art Set", "Paint Brush", "Sketchbook", "Easel",
    "Yoga Mat", "Dumbbells", "Resistance Bands", "Treadmill", "Exercise Bike", "Jump Rope", "Kettlebell", "Pull-Up Bar", "Foam Roller", "Medicine Ball",
    "Sunglasses", "Backpack", "Wallet", "Belt", "Shoes", "Hat", "Scarf", "Gloves", "Jacket", "Coat",
    "Blender Bottle", "Water Bottle", "Lunch Box", "Thermos", "Cutlery Set", "Plate Set", "Glass Set", "Cooking Pot", "Frying Pan", "Knife Set",
    "Carpet", "Curtains", "Pillow", "Blanket", "Bed Sheet", "Mattress", "Lamp Shade", "Wall Clock", "Picture Frame", "Mirror",
    "Smart Door Lock", "Security Camera", "Smoke Detector", "Carbon Monoxide Detector", "Motion Sensor", "Alarm System", "Doorbell Camera", "Window Sensor", "Smart Lock", "Garage Door Opener",
    "Plant Pot", "Garden Shovel", "Watering Can", "Hose", "Lawn Mower", "Rake", "Pruner", "Gloves Garden", "Wheelbarrow", "Fertilizer",
    "Tent", "Sleeping Bag", "Backpacking Stove", "Camping Lantern", "Hiking Boots", "Compass", "Binoculars", "Fishing Rod", "Fishing Reel", "Tackle Box",
    "Skateboard", "Roller Skates", "Bicycle Helmet", "Knee Pads", "Elbow Pads", "Sports Jersey", "Soccer Ball", "Basketball", "Volleyball", "Tennis Racket",
    "Drone Battery", "Camera Tripod", "Lens Filter", "Micro SD Card", "External SSD", "Wireless Charger", "Smart Speaker", "Projector Screen", "VR Controller", "Gaming Mouse",
    "Desk Organizer", "Cable Management", "USB Hub", "Laptop Stand", "Monitor Arm", "Chair Mat", "Foot Rest", "Keyboard Tray", "Mouse Pad", "Headset Stand",
    "Electric Grill", "Deep Fryer", "Ice Cream Maker", "Popcorn Maker", "Waffle Maker", "Sandwich Maker", "Food Steamer", "Electric Skillet", "Coffee Grinder", "Espresso Machine",
    "Air Fryer", "Rice Cooker", "Slow Cooker", "Bread Maker", "Pressure Cooker", "Water Purifier", "Juicer", "Blender", "Mixer", "Hand Mixer",
    "Vacuum Robot", "Upright Vacuum", "Handheld Vacuum", "Steam Mop", "Car Vacuum", "Window Cleaner", "Air Purifier", "Dehumidifier", "Humidifier", "Fan Tower"
]
categories = [
    "Office", "Electronics", "Home Appliances", "Kitchen", "Audio", "Computers", "Mobile Devices", "Photography", "Wearables", "Entertainment",
    "Cleaning", "Heating and Cooling", "Networking", "Storage", "Furniture", "Stationery", "Toys", "Fitness", "Clothing", "Accessories",
    "Outdoor", "Camping", "Gardening", "Sports", "Gaming", "Smart Home", "Security", "Lighting", "Travel", "Cooking",
    "Health", "Personal Care", "Baby", "Pet Supplies", "Automotive", "Beverage", "Food Prep", "Home Decor", "Bedding", "Bath",
    "DIY", "Tools", "Office Electronics", "Office Furniture", "Gaming Accessories", "Photography Accessories", "Video", "Audio Equipment", "Networking Devices", "Home Entertainment",
    "Cleaning Appliances", "Kitchen Appliances", "Small Appliances", "Wearable Tech", "Mobile Accessories", "Computer Accessories", "Printer Supplies", "Storage Devices", "Power Tools", "Garden Tools",
    "Fitness Equipment", "Sports Gear", "Outdoor Equipment", "Camping Gear", "Travel Accessories", "Bags", "Footwear", "Clothing Accessories", "Home Improvement", "Electrical",
    "Lighting Fixtures", "Home Decor Items", "Furniture Accessories", "Bedding and Linens", "Bath Accessories", "Pet Care", "Food Storage", "Cooking Tools", "Drinkware", "Serveware",
    "Plates and Bowls", "Cutlery", "Glassware", "Coffee and Tea", "Juicers and Blenders", "Microwaves", "Ovens", "Toasters", "Grills", "Deep Fryers",
    "Slow Cookers", "Rice Cookers", "Bread Makers", "Pressure Cookers", "Ice Cream Makers", "Popcorn Makers", "Waffle Makers", "Sandwich Makers", "Food Steamers", "Hand Mixers",
    "Vacuum Cleaners", "Robotic Vacuums", "Steam Mops", "Air Purifiers", "Dehumidifiers", "Humidifiers", "Fans", "Heaters", "Air Conditioners", "Lighting Accessories",
    "Smart Plugs", "Smart Lights", "Smart Thermostats", "Smart Locks", "Security Cameras", "Doorbell Cameras", "Motion Sensors", "Smoke Detectors", "Carbon Monoxide Detectors", "Garage Openers",
    "Garden Pots", "Watering Equipment", "Lawn Tools", "Pruning Tools", "Fertilizers", "Seeds", "Compost", "Hoses", "Wheelbarrows", "Outdoor Furniture",
    "Tents", "Sleeping Bags", "Backpacking Gear", "Camping Stoves", "Lanterns", "Hiking Gear", "Binoculars", "Fishing Gear", "Sports Balls", "Rackets",
    "Protective Gear", "Skateboards", "Roller Skates", "Bicycles", "Helmets", "Safety Gear", "Gaming Consoles", "Game Controllers", "VR Gear", "Projectors",
    "Tripods", "Camera Lenses", "Memory Cards", "External Drives", "Chargers", "Docking Stations", "Monitor Stands", "Keyboard Trays", "Mouse Pads", "Headset Stands",
    "Coffee Machines", "Blenders", "Mixers", "Juicers", "Food Processors", "Electric Grills", "Toasters", "Microwave Ovens", "Rice Cookers", "Pressure Cookers",
    "Vacuum Robots", "Upright Vacuums", "Handheld Vacuums", "Steam Mops", "Fans", "Air Purifiers", "Humidifiers", "Dehumidifiers", "Heaters", "Air Conditioners",
    "Smart Watches", "Fitness Trackers", "VR Headsets", "Drones", "Action Cameras", "Bluetooth Speakers", "Smart Phones", "Tablets", "Laptops", "Desktops"
]

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "category", "price", "quantity"])

    error_count = 0

    for i in range(num_records):
        is_error = random.random() < ERROR_RATE

        name = random.choice(names)
        category = random.choice(categories)
        price = round(random.uniform(10, 2000), 2)
        quantity = random.randint(1, 500)

        if is_error:
            error_count += 1
            error_type = random.choice([
                "price_text",
                "quantity_missing",
                "missing_column",
                "negative_price",
                "garbage_row"
            ])

            if error_type == "price_text":
                writer.writerow([name, category, "abc", quantity])

            elif error_type == "quantity_missing":
                writer.writerow([name, category, price, ""])

            elif error_type == "missing_column":
                writer.writerow([name, category, price])

            elif error_type == "negative_price":
                writer.writerow([name, category, -price, quantity])

            elif error_type == "garbage_row":
                writer.writerow(["###", None, "???", "xxx"])

        else:
            writer.writerow([name, category, price, quantity])

print(f"CSV '{filename}' created.")
print(f"Total records: {num_records}")
print(f"Errors generated: {error_count} (~{ERROR_RATE * 100}%)")