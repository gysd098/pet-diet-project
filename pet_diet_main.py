import streamlit as st
import random

ingredients = {'protein':['Beef, Ground','Beef, Eye of round','Beef London broil','Bison, Ground', 'Chicken Ground','Chiken Canned breast','Cod Filet','Lamb','Pork', 'Tuna','Turkey'],
            'carbohydrate':['Barley','Couscous','Macaroni noodles','Millet','Rice(brown or while)','Potatoes with peels','Potatoes without peels'],
            'vegetable_oil':['Non-GMO Soybean Oil'],
            'Veggie Snacks':['Carrots','Broccoli','Cucumber','Green beans', 'Cauliflower','Squash','Peppers','Tomatoes','Peas'],
            'Fruit Snacks':['Apples','Bananas','Berries','Melon','Pears','Peaches','Pineapple','Plums','Strawberries']}

allergy_list = ['Chicken', 'Beef', 'Lamb', 'Pork', 'Turkey']
# 'Eggs', 'Dairy','Wheat', 'Corn', 'Soy']

protein_allergy_dict = {
   'Chicken':['Chicken Ground','Chiken Canned breast'],
   'Beef':['Beef, Ground','Beef, Eye of round','Beef London broil','Bison, Ground'],
   'Lamb':['Lamb'],
   'Pork':['Pork'],
   'Turkey':['Turkey']
}


# 질병별 영양 비율 및 제한 정의
disease_diet_profiles = {
    "알러지": {
        "carb_ratio": 0.5,
        "protein_ratio": 0.5
    },
    "관절염": {
        "carb_ratio": 0.6,
        "protein_ratio": 0.4
    },
    "방광염/요로계 질환": {
        "carb_ratio": 0.6,
        "protein_ratio": 0.4
    },
    "암": {
        "carb_ratio": 0.3,
        "protein_ratio": 0.5
    },
    "치과질환": {
        "carb_ratio": 0.5,
        "protein_ratio": 0.5
    },
    "당뇨병": {
        "carb_ratio": 0.4,
        "protein_ratio": 0.6
    },
    "심장병": {
        "carb_ratio": 0.5,
        "protein_ratio": 0.5
    },
    "간질환": {
        "carb_ratio": 0.6,
        "protein_ratio": 0.3
    },
    "비만": {
        "carb_ratio": 0.6,
        "protein_ratio": 0.3
    },
    "췌장염": {
        "carb_ratio": 0.6,
        "protein_ratio": 0.3,
        "low_fat": True
    },
    "갑상선 기능저하증": {
        "carb_ratio": 0.5,
        "protein_ratio": 0.4
    },
    "간질": {
        "carb_ratio": 0.3,
        "protein_ratio": 0.5
    },
    "신장 질환": {
        "carb_ratio": 0.7,
        "protein_ratio": 0.3,
        "limit_protein": True
    }
}

st.title("반식추🐶")
st.subheader("반려동물 식단 추천")

# 이름쓰는 칸 만들기
name = st.text_input("이름을 입력하세요")
# 나이 적는 칸 만들기
age = st.number_input("나이(개월)를 입력하세요(숫자만 입력하세요)")

# 몸무게 칸
weight = st.number_input("몸무게(kg)를 입력하세요")

# 중성화 여부
neutering = st.radio("중성화 여부", ['O','X'])

# 체중감량 필요 여부
need_diet = st.radio("체중감량이 필요한가요?", ['O','X'])

# 임신중
preg = st.radio("임신중이거나 수유중인가요?", ['임신중','수유중','해당없음'])

# 활동성 : low, normal, high
activity = st.radio("활동량은 어떤가요?", ["low", "normal", "high"])

# 산책 몇시간 하는지?
time = st.number_input("하루 평균 산책시간은 어떻게 되나요? (시간)")

if time >= 1:
    final_activity = 'normal'
elif time >= 2:
    final_activity = 'high'
else: 
    final_activity = activity

# 알러지 : chicken, beef, wheat, egg, fish
selected_allergy_list = st.multiselect("알러지가 있나요?", allergy_list)

# 질병 : None, Kidney issues, Liver issues, Diabetes, 
# 슬개골 탈구, 허리디스크, 쿠싱 증후군 
disease_list = [ "관절염", "방광염/요로계 질환", "암", "치과질환", "당뇨병", 
'심장병', '간질환','비만','췌장염','갑상선 기능저하증','간질', '신장 질환']

disease = st.multiselect("질병을 앓고 있나요? 앓고 있는 질병 모두 선택해주세요", disease_list)
# disease ['간질','비만']

# calculate af
# 체중감량 1.0 
# 강아지 2-4개월 3.0
# 강아지 4-12개월 2.0
# 임신 1.8 
# 수유기 4.0

# 노령견 1.2
# 중성화된 성견(정상활동) 1.6
# 비중성화 성견 (활동적) 1.8

# 매우 활동적 2.5
af = 1.6
if need_diet == 'O':
    af = 1.0 
elif age >=2 and age <= 4:
    af = 3.0
elif age >=4 and age <= 12:
    if final_activity == 'high':
        af = 2.5
    else:
        af = 2.0
elif preg == '임신중':
    af = 1.8
elif preg == '수유중':
    af = 4.0 
elif age >=120:
    af = 1.2 
elif neutering == 'O':
    af = 1.8
elif final_activity == 'high':
    af = 2.5




if st.button("식단추천"):
    st.success("식단추천해드릴게요!")
    # calculate rer & mer
    mer = 0
    if weight > 0 :
        rer = 70 * weight ** 0.75
        mer = round(rer * af)
        st.success(f"{name}의 하루 에너지 요구량은 {mer}kcal")
    else:
        st.warning("enter weight")
    if mer > 0 :
        if len(disease) == 0 :
            carb_avg = 0.5
            protein_avg = 0.5
        else:
            # 탄수화물과 단백질 비율 계산
            # 단백질과 탄수화물 각각 한개씩 추천
            carb_sum = 0 
            protein_sum = 0 
            for d in disease:
                carb_sum += disease_diet_profiles[d]['carb_ratio']
                protein_sum = disease_diet_profiles[d]['protein_ratio']
            carb_avg = carb_sum/len(disease)  #0.4
            protein_avg = protein_sum/len(disease) #0.3
            #0.4/0.7 = 0.57
            #0.3/0.7 = 0.42

        final_carb_ratio = carb_avg/ (carb_avg+protein_avg)
        final_protein_ratio = protein_avg/ (carb_avg+protein_avg)

        carb_g = mer * final_carb_ratio/4
        protein_g = mer * final_protein_ratio/4
        
        allergy_ingredient_list = []
        for all in selected_allergy_list:
            allergy_ingredient_list = allergy_ingredient_list+ protein_allergy_dict[all]
        print(allergy_ingredient_list)

        protein_list = list(set(ingredients['protein']) - set(allergy_ingredient_list))

        protein_item = random.choice(protein_list)

        carb_item = random.choice(ingredients['carbohydrate'])
        snack_item = random.choice(ingredients['Veggie Snacks']+ ingredients['Fruit Snacks'])
        

        # 결과 출력
        st.write(f"🍖 **Recommand Protein**: {protein_item},{int(protein_g)}g")
        st.write(f"🍚 **Recommand Carbohydrate**: {carb_item},{int(carb_g)}g")
        st.write(f"🍚 **Recommand Snacks**: {snack_item}")
    else:
        st.write(f"Please enter weight for calculating MER")
# cabo : potato 100g 
#        rice 200g
# pro: chicken 100g 
#     duck 100g 
# fat : olive oil 10g 
#  [recommand today's meal]
#  rice 200g, duck 100g, olive oil 10g 
