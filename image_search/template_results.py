"""
Template results used in image search. Includes
- default_result: displayed when user first lands on image search page.
- no_similar_result: displayed if there are no similar images.
- bad_format_result: displayed if the image uploaded is of incorrect format.
- empty_submit_result: displayed if user clicks submit without selecting an image.
"""
default_result = {0: ('data/images/train_top_level/Sports & Outdoors/B00INYMGAW.jpg',
                      'Oakley Flak Jacket XLJ 03-917 Polished White/Black Iridium Sunglasses',
                      'Sports & Outdoors -> Accessories -> Sports Sunglasses'),
                  1: ('data/images/train_top_level/Clothing, Shoes & Jewelry/B00FHL1ZZG.jpg',
                      'Doublju Super Slim Contrast Drawstring Color Athletic Zip-Up Hoodie',
                      'Clothing, Shoes & Jewelry -> Men -> Clothing -> Fashion Hoodies & Sweatshirts'),
                  2: ('data/images/train_top_level/Cell Phones & Accessories/B00KEGYXV2.jpg',
                      'Vinsic Tulip 3200mAh Power Bank, 5V 1A External Mobile Battery Charger Pack for iPhone, '
                      'iPad, iPod, Samsung Devices, Cell Phones, Tablet PCs (Black)',
                      'Cell Phones & Accessories -> Accessories -> Batteries -> External Battery Packs'),
                  3: ('data/images/train_top_level/Home & Kitchen/B00I52XP5M.jpg',
                      'LexMod Engage Wood Loveseat, Azure',
                      'Home & Kitchen -> Furniture -> Living Room Furniture -> Sofas & Couches'),
                  4: ('data/images/train_top_level/Toys & Games/B001SEQQB4.jpg',
                      'Power Wheels Kawasaki KFX with Monster Traction, Normal',
                      'Toys & Games -> Tricycles, Scooters & Wagons -> Ride-On Toys'),
                  5: ('data/images/train_top_level/Clothing, Shoes & Jewelry/B00JMX1HMG.jpg',
                      'Styluxe Womens LAM Closed Round Toe Cut Out Perforated High Heel Hidden Platform Stiletto '
                      'Pump Shoes',
                      'Clothing, Shoes & Jewelry -> Women -> Shoes -> Pumps'),
                  6: ('data/images/train_top_level/Tools & Home Improvement/B00ANT5D50.jpg',
                      'Pink Lilic Resemble Art Nouveau Table Lamp OK-2502PP',
                      'Tools & Home Improvement -> Lighting & Ceiling Fans -> Lamps & Shades -> Table Lamps'),
                  7: ('data/images/train_top_level/Electronics/B00005S8KM.jpg',
                      'Sennheiser  HD 580 Dynamic HiFi Professional Headphone',
                      'Electronics -> Accessories & Supplies -> Audio & Video Accessories -> Headphones'),
                  8: ('data/images/train_top_level/Office Products/B00FWMNF26.jpg',
                      'DX Racer Office Chair Computer Seat Gaming Chair OH/FD56',
                      'Office Products -> Office Furniture & Lighting -> Chairs & Sofas -> Desk Chairs')}

no_similar_result = {1: ('data/images/train_top_level/Toys & Games/B00005201N.jpg',
                         'Sorry, no similar products. Please try another image!',
                         'Sad Panda')}

bad_format_result = {0: ('data/images/train_top_level/Toys & Games/B003CTH3TW.jpg',
                         'Image should have .png, .jpg, or .jpeg extension (case-insensitive).',
                         'Shy Domo')}

empty_submit_result = {0: ('data/images/train_top_level/Toys & Games/B004FVWH1K.jpg',
                           'Browse for an image before submitting!',
                           'Helpful Pikachu')}
