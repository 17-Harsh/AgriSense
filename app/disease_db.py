"""
AgriSense Disease Knowledge Base
Contains detailed information about crop diseases, symptoms, treatments,
and prevention strategies sourced from agricultural research databases.
"""

DISEASE_INFO = {
    'Apple___Apple_scab': {
        'crop': 'Apple',
        'disease': 'Apple Scab',
        'pathogen': 'Venturia inaequalis (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Apple scab is one of the most common and economically damaging '
            'diseases of apple trees. The fungus overwinters in fallen infected '
            'leaves and produces spores in spring that are carried by wind and rain.'
        ),
        'symptoms': [
            'Olive-green to brown velvety spots on leaves',
            'Dark, scabby lesions on fruit surface',
            'Premature leaf drop in severe cases',
            'Distorted and cracked fruit when infected early',
        ],
        'treatment': [
            'Apply fungicides such as Mancozeb or Captan at bud break',
            'Continue fungicide applications at 7-10 day intervals through wet periods',
            'Use systemic fungicides like Myclobutanil for curative action',
            'Remove and destroy infected leaves and fruit drops',
        ],
        'prevention': [
            'Plant scab-resistant varieties (Liberty, Enterprise, GoldRush)',
            'Ensure good air circulation by proper pruning',
            'Apply urea spray to fallen leaves in autumn to speed decomposition',
            'Avoid overhead irrigation to reduce leaf wetness duration',
        ],
        'fertilizer': 'Apply balanced NPK (10-10-10) fertilizer in early spring. Add calcium sprays to strengthen cell walls.',
    },
    'Apple___Black_rot': {
        'crop': 'Apple',
        'disease': 'Black Rot',
        'pathogen': 'Botryosphaeria obtusa (Fungus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Black rot affects fruit, leaves, and bark of apple trees. '
            'The fungus can cause significant economic losses through fruit rot '
            'and cankers on branches that girdle and kill limbs.'
        ),
        'symptoms': [
            'Purple or reddish-brown spots on leaves (frogeye leaf spot)',
            'Large brown rotting areas on fruit starting from blossom end',
            'Concentric rings visible on rotted fruit',
            'Sunken cankers on branches with reddish-brown bark',
        ],
        'treatment': [
            'Prune out dead wood and cankers during dormant season',
            'Apply Captan or Thiophanate-methyl fungicides',
            'Remove mummified fruit from trees and ground',
            'Treat wounds with fungicidal paste',
        ],
        'prevention': [
            'Maintain good tree vigor with proper nutrition',
            'Remove fire blight-killed wood promptly',
            'Keep orchard floor clean of debris',
            'Practice proper sanitation after pruning',
        ],
        'fertilizer': 'Apply potassium-rich fertilizer to improve disease resistance. Use foliar sprays of micronutrients (Zinc, Boron).',
    },
    'Apple___Cedar_apple_rust': {
        'crop': 'Apple',
        'disease': 'Cedar Apple Rust',
        'pathogen': 'Gymnosporangium juniperi-virginianae (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'This rust disease requires two hosts to complete its lifecycle — '
            'cedar/juniper trees and apple trees. Orange gelatinous galls '
            'on cedars release spores that infect apple trees in spring.'
        ),
        'symptoms': [
            'Bright yellow-orange spots on upper leaf surface',
            'Tube-like structures (aecia) on corresponding lower leaf surface',
            'Similar lesions on fruit causing deformation',
            'Severe defoliation in heavy infection years',
        ],
        'treatment': [
            'Apply fungicides containing Myclobutanil at pink bud stage',
            'Continue applications through petal fall',
            'Use Mancozeb as a protectant fungicide',
            'Remove nearby cedar trees if feasible (within 2-3 miles)',
        ],
        'prevention': [
            'Plant rust-resistant apple varieties',
            'Remove galls from nearby cedar trees before spring',
            'Maintain adequate spacing between apple and cedar trees',
            'Scout for early symptoms starting at bloom',
        ],
        'fertilizer': 'Apply balanced NPK with additional phosphorus for root strength. Foliar calcium applications help resist infection.',
    },
    'Apple___healthy': {
        'crop': 'Apple',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your apple plant appears healthy. Continue with regular maintenance and monitoring.',
        'symptoms': [],
        'treatment': ['No treatment required. Continue regular maintenance.'],
        'prevention': [
            'Maintain proper irrigation schedule',
            'Apply balanced fertilizers seasonally',
            'Prune regularly for air circulation',
            'Monitor for early signs of disease',
        ],
        'fertilizer': 'Apply balanced NPK (10-10-10) in early spring. Add compost and organic matter annually.',
    },
    'Corn___Cercospora_leaf_spot': {
        'crop': 'Corn (Maize)',
        'disease': 'Cercospora Leaf Spot (Gray Leaf Spot)',
        'pathogen': 'Cercospora zeae-maydis (Fungus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Gray leaf spot is one of the most significant foliar diseases '
            'of corn worldwide. It thrives in warm, humid conditions and can '
            'cause yield losses of 20-40% in severe outbreaks.'
        ),
        'symptoms': [
            'Small rectangular lesions bounded by leaf veins',
            'Lesions are grey to tan colored',
            'Lesions may coalesce causing large areas of leaf blight',
            'Lower leaves affected first, progressing upward',
        ],
        'treatment': [
            'Apply foliar fungicides such as Azoxystrobin or Propiconazole',
            'Time applications at VT to R1 growth stage for best results',
            'Consider tank-mixing strobilurin and triazole fungicides',
            'Apply fungicide when disease reaches third leaf below ear',
        ],
        'prevention': [
            'Plant resistant hybrids with high GLS resistance ratings',
            'Rotate crops — avoid continuous corn planting',
            'Tillage to bury infected crop residue',
            'Improve field drainage and air movement',
        ],
        'fertilizer': 'Apply nitrogen at recommended rates (180-220 kg/ha). Avoid excess nitrogen which increases susceptibility. Add potassium for disease tolerance.',
    },
    'Corn___Common_rust': {
        'crop': 'Corn (Maize)',
        'disease': 'Common Rust',
        'pathogen': 'Puccinia sorghi (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Common rust of corn is caused by the fungus Puccinia sorghi. '
            'It is most prevalent in cooler, humid weather and rarely causes '
            'severe losses in field corn, though sweet corn is more susceptible.'
        ),
        'symptoms': [
            'Small, circular to elongated cinnamon-brown pustules on both leaf surfaces',
            'Pustules break through the leaf epidermis releasing powdery spores',
            'Severely infected leaves may turn yellow and die',
            'Pustules may also appear on husks and leaf sheaths',
        ],
        'treatment': [
            'Apply fungicides containing Propiconazole or Mancozeb at first sign',
            'Foliar fungicide application if >50% of plants show pustules before tasseling',
            'Sweet corn may require earlier and more frequent applications',
            'Strobilurin fungicides provide both preventive and curative activity',
        ],
        'prevention': [
            'Plant resistant hybrids with Rp genes for rust resistance',
            'Early planting to avoid peak spore dispersal periods',
            'Maintain balanced nutrition to support plant defenses',
            'Scout regularly from V8 stage onwards',
        ],
        'fertilizer': 'Apply recommended NPK rates. Ensure adequate potassium (120-150 kg/ha K2O) for disease resistance.',
    },
    'Corn___Northern_Leaf_Blight': {
        'crop': 'Corn (Maize)',
        'disease': 'Northern Leaf Blight',
        'pathogen': 'Exserohilum turcicum (Fungus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Northern corn leaf blight is a significant disease that can '
            'cause yield losses of 30-50% under favorable conditions. The '
            'fungus survives on crop residue and produces spores during warm, humid weather.'
        ),
        'symptoms': [
            'Large, elliptical cigar-shaped lesions (2.5-15 cm long)',
            'Lesions are grayish-green to tan colored',
            'Lower leaves affected first, progressing upward',
            'Severe infection leads to large areas of dead tissue',
        ],
        'treatment': [
            'Apply foliar fungicides at tasseling stage (VT-R1)',
            'Use strobilurin-based fungicides (Azoxystrobin, Pyraclostrobin)',
            'Tank mix with triazole fungicides for resistance management',
            'Reapply if conditions remain favorable 14-21 days after first application',
        ],
        'prevention': [
            'Plant hybrids with Ht gene resistance',
            'Rotate crops with soybeans or other non-host crops',
            'Bury crop residue through tillage',
            'Avoid late planting dates',
        ],
        'fertilizer': 'Apply balanced NPK with emphasis on potassium for disease tolerance. Foliar silicon sprays may enhance resistance.',
    },
    'Corn___healthy': {
        'crop': 'Corn (Maize)',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your corn plant appears healthy. Continue monitoring for proper growth and development.',
        'symptoms': [],
        'treatment': ['No treatment required. Continue regular crop management.'],
        'prevention': [
            'Follow recommended planting density',
            'Apply fertilizers based on soil test results',
            'Practice crop rotation annually',
            'Scout for pests and diseases weekly',
        ],
        'fertilizer': 'Apply nitrogen in split doses (at planting and V6). Ensure phosphorus and potassium are adequate based on soil tests.',
    },
    'Grape___Black_rot': {
        'crop': 'Grape',
        'disease': 'Black Rot',
        'pathogen': 'Guignardia bidwellii (Fungus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Grape black rot is a devastating disease of grapes that can '
            'destroy an entire crop within days of symptoms appearing. '
            'The fungus thrives in warm, humid conditions.'
        ),
        'symptoms': [
            'Small reddish-brown circular leaf spots with dark borders',
            'Black pycnidia (fruiting bodies) visible in leaf spots',
            'Fruit turns brown, shrivels into hard black mummies',
            'Infected tendrils and shoots show dark elongated lesions',
        ],
        'treatment': [
            'Apply Mancozeb or Captan fungicides from bud break through veraison',
            'Use Myclobutanil or similar DMI fungicides for curative action',
            'Increase spray frequency during wet weather',
            'Remove mummified fruit and infected canes',
        ],
        'prevention': [
            'Remove and destroy mummified berries from vines and ground',
            'Train and trellis vines for good air circulation',
            'Prune to open canopy and improve drying conditions',
            'Begin fungicide program at early shoot growth',
        ],
        'fertilizer': 'Moderate nitrogen application to avoid excessive vegetative growth. Balanced potassium and calcium for strong berry skins.',
    },
    'Grape___Esca_(Black_Measles)': {
        'crop': 'Grape',
        'disease': 'Esca (Black Measles)',
        'pathogen': 'Complex of fungi including Phaeomoniella, Phaeoacremonium',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Esca is a complex disease associated with multiple wood-inhabiting fungi. '
            'It can cause sudden collapse of vines (apoplexy) or chronic decline. '
            'The disease is becoming increasingly prevalent worldwide.'
        ),
        'symptoms': [
            'Tiger-stripe pattern on leaves (interveinal chlorosis and necrosis)',
            'Dark spots on berries resembling measles',
            'Internal wood decay visible as dark streaking in cross-section',
            'Sudden vine death (apoplexy) during hot weather',
        ],
        'treatment': [
            'No fully effective cure exists; manage symptoms',
            'Trunk surgery to remove infected wood in valuable vines',
            'Apply Trichoderma-based biological products to pruning wounds',
            'Sodium arsenite (where allowed by regulations) as dormant treatment',
        ],
        'prevention': [
            'Protect pruning wounds with fungicidal paste or Trichoderma products',
            'Delay pruning to late dormant season when possible',
            'Avoid large pruning wounds',
            'Use certified disease-free planting material',
        ],
        'fertilizer': 'Balanced nutrition to maintain vine vigor. Avoid water stress which triggers apoplexy symptoms.',
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'crop': 'Grape',
        'disease': 'Leaf Blight (Isariopsis Leaf Spot)',
        'pathogen': 'Pseudocercospora vitis (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Isariopsis leaf spot causes significant defoliation in table and '
            'wine grapes, particularly in tropical and subtropical regions. '
            'It thrives in warm, humid conditions with frequent rainfall.'
        ),
        'symptoms': [
            'Dark brown to black irregular spots on leaves',
            'Spots may have yellowish borders (halos)',
            'Severe infection causes premature defoliation',
            'Spots typically start on lower leaves and progress upward',
        ],
        'treatment': [
            'Apply copper-based fungicides (Bordeaux mixture)',
            'Use Mancozeb or Zineb as protectant fungicides',
            'Apply Carbendazim for systemic control',
            'Spray at 10-14 day intervals during wet weather',
        ],
        'prevention': [
            'Improve vineyard air circulation through canopy management',
            'Remove and destroy fallen infected leaves',
            'Ensure adequate vine spacing for air movement',
            'Avoid excessive nitrogen fertilization',
        ],
        'fertilizer': 'Apply NPK (10-26-26) to promote fruiting over vegetative growth. Foliar zinc and manganese sprays enhance disease resistance.',
    },
    'Grape___healthy': {
        'crop': 'Grape',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your grape vine appears healthy. Maintain current vineyard management practices.',
        'symptoms': [],
        'treatment': ['No treatment required.'],
        'prevention': [
            'Continue regular canopy management',
            'Maintain balanced irrigation',
            'Monitor for early disease signs',
            'Keep vineyard floor clean',
        ],
        'fertilizer': 'Apply compost in winter. Balanced NPK in early spring with micronutrient supplements.',
    },
    'Potato___Early_blight': {
        'crop': 'Potato',
        'disease': 'Early Blight',
        'pathogen': 'Alternaria solani (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Early blight is a common foliar disease of potato that typically '
            'appears mid-season. It causes concentric ring lesions on leaves '
            'that merge and cause significant defoliation, reducing yield by 20-30%.'
        ),
        'symptoms': [
            'Dark brown to black spots with concentric rings (target board pattern)',
            'Yellowing of tissue around spots',
            'Lesions typically appear first on older lower leaves',
            'Tuber lesions appear as dark, sunken, circular spots',
        ],
        'treatment': [
            'Apply fungicides containing Chlorothalonil or Mancozeb',
            'Use systemic fungicides like Azoxystrobin or Difenoconazole',
            'Begin applications when first symptoms appear',
            'Maintain 7-day spray schedule during favorable conditions',
        ],
        'prevention': [
            'Plant certified disease-free seed tubers',
            'Practice 3-year crop rotation',
            'Adequate hilling to protect tubers from spores',
            'Maintain balanced nutrition — avoid nitrogen deficiency',
        ],
        'fertilizer': 'Apply adequate nitrogen (200-250 kg/ha) in split doses. Balanced potassium improves disease resistance. Calcium amendments reduce tuber susceptibility.',
    },
    'Potato___Late_blight': {
        'crop': 'Potato',
        'disease': 'Late Blight',
        'pathogen': 'Phytophthora infestans (Oomycete)',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Late blight is the most devastating potato disease worldwide. '
            'It was responsible for the Irish Potato Famine (1845-1849). '
            'Under favorable conditions, it can destroy an entire field within a week.'
        ),
        'symptoms': [
            'Water-soaked, dark green to brown lesions on leaf edges and tips',
            'White fuzzy mold growth on underside of infected leaves in humid conditions',
            'Stem lesions appear as dark brown to black areas',
            'Tubers show brown, granular rot extending from surface',
        ],
        'treatment': [
            'Apply protectant fungicides (Mancozeb, Chlorothalonil) preventively',
            'Use systemic fungicides (Metalaxyl, Cymoxanil) — check for resistance',
            'Spray at 5-7 day intervals during high-risk periods',
            'Destroy infected plant material immediately',
        ],
        'prevention': [
            'Use certified late blight-free seed potatoes',
            'Plant resistant varieties (Sarpo Mira, Defender)',
            'Destroy all volunteer potato plants and cull piles',
            'Monitor weather forecasts — blight risk models available',
        ],
        'fertilizer': 'Balanced NPK with emphasis on potassium (K) for disease resistance. Avoid excess nitrogen. Apply calcium-based amendments.',
    },
    'Potato___healthy': {
        'crop': 'Potato',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your potato plant appears healthy. Continue regular crop management.',
        'symptoms': [],
        'treatment': ['No treatment required.'],
        'prevention': [
            'Continue proper irrigation management',
            'Hill soil around plants as they grow',
            'Monitor for pests and diseases weekly',
            'Use certified seed potatoes',
        ],
        'fertilizer': 'Apply balanced NPK based on soil test. Side-dress nitrogen at tuber initiation stage.',
    },
    'Rice___Brown_spot': {
        'crop': 'Rice',
        'disease': 'Brown Spot',
        'pathogen': 'Bipolaris oryzae (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Brown spot is a widespread rice disease associated with nutrient-deficient soils. '
            'It was the primary cause of the Bengal Famine of 1943. '
            'The disease causes both leaf spots and grain discoloration.'
        ),
        'symptoms': [
            'Circular to oval brown spots on leaves with gray centers',
            'Spots typically 5-14 mm long on mature leaves',
            'Grain discoloration and spotting on glumes',
            'Seedling blight in severe cases',
        ],
        'treatment': [
            'Apply Propiconazole or Carbendazim fungicides',
            'Seed treatment with Tricyclazole or Thiram before sowing',
            'Foliar spray of Mancozeb at tillering and panicle initiation',
            'Apply potassium fertilizer to reduce severity',
        ],
        'prevention': [
            'Use resistant varieties and certified disease-free seed',
            'Maintain adequate and balanced soil fertility',
            'Proper water management — avoid stress conditions',
            'Treat seeds with hot water (52°C for 10 minutes)',
        ],
        'fertilizer': 'Apply balanced NPK with emphasis on potassium and silicon. Correct micronutrient deficiencies, especially zinc and manganese.',
    },
    'Rice___Leaf_blast': {
        'crop': 'Rice',
        'disease': 'Leaf Blast',
        'pathogen': 'Magnaporthe oryzae (Fungus)',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Rice blast is the most destructive disease of rice globally, '
            'causing annual losses of 10-30% of production. '
            'It can affect leaves, nodes, stems, and panicles at any growth stage.'
        ),
        'symptoms': [
            'Diamond or spindle-shaped spots with gray centers on leaves',
            'Spots have dark brown borders and may coalesce',
            'Infected areas expand rapidly during humid weather',
            'Whitehead — completely blank panicles when neck is infected',
        ],
        'treatment': [
            'Apply Tricyclazole as preventive spray (most effective)',
            'Use Isoprothiolane or Kasugamycin for curative action',
            'Begin spraying at first sign of disease',
            'Apply at tillering and heading stages preventively',
        ],
        'prevention': [
            'Plant blast-resistant varieties (check local recommendations)',
            'Avoid excessive nitrogen application',
            'Maintain continuous flooding (avoid drought stress)',
            'Use silicon-rich fertilizers to strengthen cell walls',
        ],
        'fertilizer': 'Reduce nitrogen to recommended levels. Apply silicon (200 kg/ha silicate). Balanced potassium for disease tolerance.',
    },
    'Rice___Neck_blast': {
        'crop': 'Rice',
        'disease': 'Neck Blast',
        'pathogen': 'Magnaporthe oryzae (Fungus)',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Neck blast is the most damaging form of rice blast disease. '
            'The infection at the panicle base causes the entire panicle to '
            'turn white (whitehead) and produce empty or partially filled grains.'
        ),
        'symptoms': [
            'Grayish brown lesion at the neck node (panicle base)',
            'Panicle breakage at infected neck node',
            'Whiteheads — panicles with unfilled chalky grains',
            'Complete panicle death in severe cases',
        ],
        'treatment': [
            'Preventive Tricyclazole spray at 5% heading is critical',
            'Second spray at 50% heading for extended protection',
            'Isoprothiolane as alternative systemic fungicide',
            'Combination of Tricyclazole + Propiconazole for severe outbreaks',
        ],
        'prevention': [
            'Plant blast-resistant varieties',
            'Reduce nitrogen to moderate levels',
            'Stagger planting dates to reduce inoculum pressure',
            'Destroy infected crop residue after harvest',
        ],
        'fertilizer': 'Moderate nitrogen (100-120 kg/ha). Split applications at transplanting, tillering, and panicle initiation. Apply silicon fertilizer.',
    },
    'Rice___healthy': {
        'crop': 'Rice',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your rice plant appears healthy. Continue regular paddy management.',
        'symptoms': [],
        'treatment': ['No treatment required.'],
        'prevention': [
            'Maintain proper water level in paddy field',
            'Apply fertilizers based on crop stage',
            'Monitor for pest and disease incidence',
            'Follow integrated pest management practices',
        ],
        'fertilizer': 'Apply NPK based on soil test results. Follow split application schedule for nitrogen.',
    },
    'Tomato___Bacterial_spot': {
        'crop': 'Tomato',
        'disease': 'Bacterial Spot',
        'pathogen': 'Xanthomonas campestris pv. vesicatoria (Bacteria)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Bacterial spot is a serious disease of tomato and pepper. '
            'It is favored by warm, wet weather and can cause severe defoliation '
            'and fruit spotting, reducing marketable yield significantly.'
        ),
        'symptoms': [
            'Small, water-soaked spots on leaves turning dark brown to black',
            'Spots may have yellow halos',
            'Raised, scab-like spots on fruit surface',
            'Leaf spots may merge causing large necrotic areas and defoliation',
        ],
        'treatment': [
            'Apply copper-based bactericides (copper hydroxide)',
            'Tank mix copper with Mancozeb for improved efficacy',
            'Apply at 5-7 day intervals during wet weather',
            'Streptomycin spray where permitted by regulations',
        ],
        'prevention': [
            'Use disease-free seed and transplants',
            'Avoid overhead irrigation',
            'Practice crop rotation with non-solanaceous crops',
            'Disinfect tools and equipment between fields',
        ],
        'fertilizer': 'Balanced NPK with calcium supplementation. Avoid excess nitrogen which promotes succulent growth susceptible to bacteria.',
    },
    'Tomato___Early_blight': {
        'crop': 'Tomato',
        'disease': 'Early Blight',
        'pathogen': 'Alternaria solani (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Early blight is one of the most common foliar diseases of tomatoes. '
            'The fungus survives in the soil and on crop debris, '
            'producing lesions with characteristic concentric rings.'
        ),
        'symptoms': [
            'Dark brown spots with concentric rings (target pattern) on lower leaves',
            'Yellowing around lesions',
            'Progressive defoliation from bottom of plant upward',
            'Stem lesions near soil line in seedlings (collar rot)',
        ],
        'treatment': [
            'Apply Chlorothalonil or Mancozeb fungicides at first sign',
            'Alternate with systemic fungicides (Azoxystrobin, Difenoconazole)',
            'Maintain 7-10 day spray schedule',
            'Remove and destroy infected lower leaves',
        ],
        'prevention': [
            'Use disease-free seed and transplants',
            'Mulch around plants to prevent soil splash',
            'Stake or cage plants for better air circulation',
            'Rotate crops for 3 years minimum',
        ],
        'fertilizer': 'Adequate nitrogen to maintain vigor. Calcium and potassium for disease resistance. Apply compost for soil biology.',
    },
    'Tomato___Late_blight': {
        'crop': 'Tomato',
        'disease': 'Late Blight',
        'pathogen': 'Phytophthora infestans (Oomycete)',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Late blight of tomato is a devastating disease that can destroy '
            'entire crops within days. Same pathogen responsible for the Irish '
            'Potato Famine. Requires cool, wet conditions.'
        ),
        'symptoms': [
            'Large, irregular water-soaked spots on leaves',
            'White mold growth on underside of leaves in humid conditions',
            'Stems develop dark brown to black lesions',
            'Firm, brown, greasy-looking rot on fruit',
        ],
        'treatment': [
            'Immediate application of Metalaxyl + Mancozeb (Ridomil Gold)',
            'Chlorothalonil as protectant spray',
            'Cymoxanil for curative action within 2 days of infection',
            'Remove and destroy all infected plant material',
        ],
        'prevention': [
            'Plant resistant varieties (Legend, Defiant, Iron Lady)',
            'Avoid overhead irrigation',
            'Provide good air circulation through spacing and staking',
            'Monitor late blight forecast systems',
        ],
        'fertilizer': 'Moderate nitrogen, high potassium formulation. Calcium sprays strengthen cell walls against infection.',
    },
    'Tomato___Leaf_Mold': {
        'crop': 'Tomato',
        'disease': 'Leaf Mold',
        'pathogen': 'Passalora fulva (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Leaf mold is primarily a greenhouse and high-tunnel disease '
            'that thrives in conditions of high humidity (>85%) and moderate '
            'temperatures. Open-field infections are less common.'
        ),
        'symptoms': [
            'Pale greenish-yellow spots on upper leaf surface',
            'Olive-green to grayish-purple velvety mold on lower leaf surface',
            'Infected leaves curl, wither and drop',
            'In severe cases, blossoms and fruit may also be infected',
        ],
        'treatment': [
            'Apply Chlorothalonil or Mancozeb fungicides',
            'Use systemic fungicides like Propiconazole',
            'Improve ventilation in greenhouses immediately',
            'Reduce humidity below 85% through ventilation',
        ],
        'prevention': [
            'Maintain adequate spacing between plants',
            'Improve greenhouse ventilation',
            'Avoid leaf wet periods — use drip irrigation',
            'Plant resistant varieties with Cf genes',
        ],
        'fertilizer': 'Balanced NPK with silicon supplement for leaf strength. Avoid excess nitrogen.',
    },
    'Tomato___Septoria_leaf_spot': {
        'crop': 'Tomato',
        'disease': 'Septoria Leaf Spot',
        'pathogen': 'Septoria lycopersici (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Septoria leaf spot is a common and potentially destructive disease '
            'of tomatoes occurring in warm, wet weather. '
            'It can cause severe defoliation leading to sun-scalded fruit.'
        ),
        'symptoms': [
            'Numerous small circular spots (2-3 mm) with dark borders',
            'Spots have gray or tan centers with tiny dark specks (pycnidia)',
            'Typically starts on lower leaves after fruit set',
            'Severe defoliation exposes fruit to sunscald',
        ],
        'treatment': [
            'Apply Chlorothalonil or copper-based fungicides',
            'Mancozeb provides good protectant activity',
            'Begin applications at first sign of disease',
            'Remove heavily infected lower leaves',
        ],
        'prevention': [
            'Mulch around plants to prevent rain splash from soil',
            'Stake plants and remove lower leaves for air flow',
            'Avoid working with wet plants',
            'Three-year rotation away from solanaceous crops',
        ],
        'fertilizer': 'Balanced NPK fertilization. Extra calcium helps resist infection. Foliar micronutrient sprays.',
    },
    'Tomato___Spider_mites': {
        'crop': 'Tomato',
        'disease': 'Spider Mite Damage',
        'pathogen': 'Tetranychus urticae (Two-spotted Spider Mite)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Spider mites are not a disease but a pest that causes significant damage '
            'especially in hot, dry conditions. They feed on plant cells causing '
            'stippling, bronzing, and potentially plant death.'
        ),
        'symptoms': [
            'Fine stippling (tiny yellow/white dots) on upper leaf surface',
            'Leaves turn bronze or yellow with heavy infestation',
            'Fine webbing on undersides of leaves and between leaves',
            'Leaves dry out and drop in severe infestations',
        ],
        'treatment': [
            'Apply miticides such as Abamectin or Spiromesifen',
            'Use horticultural oil or insecticidal soap for organic control',
            'Spray undersides of leaves thoroughly',
            'Release predatory mites (Phytoseiulus persimilis) for biological control',
        ],
        'prevention': [
            'Maintain adequate irrigation — water stress favors mites',
            'Avoid dusty conditions near fields',
            'Conserve natural predators — avoid broad-spectrum insecticides',
            'Monitor with 10x hand lens — check leaf undersides weekly',
        ],
        'fertilizer': 'Maintain balanced nutrition. Adequate watering is more critical than fertilization for mite management.',
    },
    'Tomato___Target_Spot': {
        'crop': 'Tomato',
        'disease': 'Target Spot',
        'pathogen': 'Corynespora cassiicola (Fungus)',
        'severity': 'Moderate',
        'severity_level': 2,
        'description': (
            'Target spot is an increasingly important disease of tomato in '
            'tropical and subtropical regions. The fungus has a wide host range '
            'and can cause severe defoliation and fruit lesions.'
        ),
        'symptoms': [
            'Small brown spots with concentric rings (target pattern)',
            'Spots enlarge and may have yellow halos',
            'Lesions can appear on leaves, stems, and fruit',
            'Severe defoliation under humid conditions',
        ],
        'treatment': [
            'Apply Chlorothalonil or Mancozeb as protectant',
            'Systemic fungicides (Azoxystrobin, Difenoconazole) for curative action',
            'Begin applications before flowering',
            'Maintain 7-14 day spray schedule',
        ],
        'prevention': [
            'Ensure adequate plant spacing',
            'Remove crop debris after harvest',
            'Use drip irrigation to avoid leaf wetness',
            'Rotate with non-host crops',
        ],
        'fertilizer': 'Moderate nitrogen with adequate potassium and calcium. Avoid imbalanced fertilization.',
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'crop': 'Tomato',
        'disease': 'Tomato Yellow Leaf Curl Virus (TYLCV)',
        'pathogen': 'TYLCV (Begomovirus), transmitted by whitefly Bemisia tabaci',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'TYLCV is one of the most devastating viral diseases of tomato worldwide. '
            'It is transmitted by the silverleaf whitefly and can cause 100% yield '
            'loss when plants are infected early in the season.'
        ),
        'symptoms': [
            'Severe upward curling and cupping of leaves',
            'Yellowing of leaf margins and interveinal areas',
            'Stunted plant growth',
            'Drastically reduced fruit set and small fruit',
        ],
        'treatment': [
            'No cure for virus — remove and destroy infected plants promptly',
            'Control whitefly vector with Imidacloprid or Thiamethoxam',
            'Use reflective mulches to repel whiteflies',
            'Apply neem oil or insecticidal soap for organic management',
        ],
        'prevention': [
            'Plant TYLCV-resistant varieties (Ty gene series)',
            'Use insect-proof netting in nurseries',
            'Install yellow sticky traps to monitor whitefly populations',
            'Remove all crop debris and alternate hosts between seasons',
        ],
        'fertilizer': 'Balanced nutrition for general plant health. Focus on vector (whitefly) control rather than fertilization.',
    },
    'Tomato___Tomato_mosaic_virus': {
        'crop': 'Tomato',
        'disease': 'Tomato Mosaic Virus (ToMV)',
        'pathogen': 'Tobamovirus (Tomato mosaic virus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Tomato mosaic virus is a highly infectious and stable virus '
            'that can persist on contaminated surfaces for years. '
            'It spreads easily through mechanical contact and contaminated seed.'
        ),
        'symptoms': [
            'Light and dark green mosaic pattern on leaves',
            'Leaf distortion and fern-like appearance (shoestring)',
            'Stunted growth in young plants',
            'Uneven fruit ripening with internal browning',
        ],
        'treatment': [
            'No chemical cure — remove infected plants immediately',
            'Sterilize tools and hands with milk solution (1:4) or TSP',
            'Do not compost infected plant material — burn or bury',
            'Treat contaminated soil with solarization',
        ],
        'prevention': [
            'Plant resistant varieties with Tm-2² resistance gene',
            'Use certified virus-free seed',
            'Avoid handling plants unnecessarily — wash hands before working',
            'Disinfect all tools, trays, and equipment between uses',
        ],
        'fertilizer': 'Standard balanced nutrition. Disease management is primarily through hygiene and resistant varieties.',
    },
    'Tomato___healthy': {
        'crop': 'Tomato',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your tomato plant appears healthy. Keep up the good work!',
        'symptoms': [],
        'treatment': ['No treatment required.'],
        'prevention': [
            'Continue regular watering schedule',
            'Maintain staking and pruning routine',
            'Monitor for pests and diseases weekly',
            'Apply balanced fertilizer every 2-3 weeks',
        ],
        'fertilizer': 'Apply balanced tomato fertilizer (5-10-10) every 2-3 weeks. Calcium supplement for blossom end rot prevention.',
    },
    'Wheat___Brown_rust': {
        'crop': 'Wheat',
        'disease': 'Brown Rust (Leaf Rust)',
        'pathogen': 'Puccinia triticina (Fungus)',
        'severity': 'High',
        'severity_level': 3,
        'description': (
            'Brown rust (leaf rust) is the most common and widely distributed '
            'rust disease of wheat. It can cause yield losses of 5-20% regularly '
            'and up to 50% in severe epidemics.'
        ),
        'symptoms': [
            'Small, circular to oval, orange-brown pustules on upper leaf surface',
            'Pustules mainly on leaves, not on stems',
            'Random scatter pattern of pustules',
            'Severe infection leads to premature leaf death',
        ],
        'treatment': [
            'Apply triazole fungicides (Propiconazole, Tebuconazole)',
            'Strobilurin fungicides provide preventive protection',
            'Apply at first sign of disease or at flag leaf emergence',
            'Single application usually sufficient if timed correctly',
        ],
        'prevention': [
            'Plant resistant varieties with Lr resistance genes',
            'Diversify resistance genes across farm',
            'Early sowing to avoid peak rust season',
            'Remove volunteer wheat and alternate hosts',
        ],
        'fertilizer': 'Balanced NPK with adequate potassium for disease resistance. Split nitrogen applications. Avoid late nitrogen.',
    },
    'Wheat___Yellow_rust': {
        'crop': 'Wheat',
        'disease': 'Yellow Rust (Stripe Rust)',
        'pathogen': 'Puccinia striiformis f. sp. tritici (Fungus)',
        'severity': 'Critical',
        'severity_level': 4,
        'description': (
            'Yellow rust (stripe rust) is one of the most destructive diseases '
            'of wheat worldwide. It favors cooler temperatures (10-15°C) with '
            'morning dew. Yield losses can reach 70-100% in susceptible varieties.'
        ),
        'symptoms': [
            'Yellow-orange pustules arranged in stripes along leaf veins',
            'Pustules form long, narrow lines parallel to veins',
            'Leaves turn yellow and dry out',
            'Glume infection leads to shriveled grain',
        ],
        'treatment': [
            'Immediately apply Propiconazole or Tebuconazole',
            'Spray at tillering and/or boot stage for best results',
            'Combine triazole + strobilurin for enhanced control',
            'Two applications may be needed in severe outbreaks',
        ],
        'prevention': [
            'Plant resistant varieties (check local Yr gene recommendations)',
            'Avoid very early sowing which extends green bridge',
            'Monitor official disease forecasts',
            'Balanced nutrition — avoid excess nitrogen',
        ],
        'fertilizer': 'Apply basal NPK with split nitrogen. Potassium sulfate for enhanced resistance. Avoid nitrogen top-dressing during active infection.',
    },
    'Wheat___healthy': {
        'crop': 'Wheat',
        'disease': 'No Disease Detected',
        'pathogen': 'N/A',
        'severity': 'None',
        'severity_level': 0,
        'description': 'Your wheat crop appears healthy. Maintain current management practices.',
        'symptoms': [],
        'treatment': ['No treatment required.'],
        'prevention': [
            'Continue monitoring for rust and other diseases',
            'Follow recommended nitrogen schedule',
            'Practice crop rotation',
            'Scout fields weekly during heading stage',
        ],
        'fertilizer': 'Apply nitrogen in 3 splits (basal, first irrigation, heading). Phosphorus and potassium based on soil test.',
    },
}
