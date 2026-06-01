import google.generativeai as genai

API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="NutriWise AI",
    page_icon="🥗",
    layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    color: #2E7D32;
}

.stButton > button {
    width: 100%;
    height: 3.2em;
    border-radius: 12px;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🥗 NutriWise AI

### Your Personal AI Nutrition & Wellness Companion

Generate customized nutrition plans tailored to:

✅ Health Conditions

✅ Local Food Availability

✅ Climate & Environment

✅ Dietary Preferences

✅ Lifestyle Factors

Powered by Google Gemini.
""")

with st.sidebar:

    st.title("🥗 NutriWise AI")

    st.markdown("---")

    st.markdown("""
### 📊 Quick Stats

🤖 **AI Model**
: Google Gemini 2.5 Flash

🌍 **Coverage**
: Global Nutrition Support

🩺 **Health Support**
: Multi-Condition Planning

🍽 **Plans**
: Daily • Weekly • Monthly
""")

    st.markdown("---")

    st.markdown("""
### 🔥 Supported Conditions

✅ Diabetes

✅ PCOS

✅ Hypertension

✅ Asthma

✅ Thyroid Disorders

✅ Obesity

✅ Vitamin Deficiencies

✅ General Wellness
""")

    st.markdown("---")

    st.info(
        """
💡 **Tip**

Provide detailed health conditions and lifestyle information for more accurate nutrition recommendations.
"""
    )
# ==================================
# USER INPUTS
# ==================================

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    city = st.text_input(
        "City",
        placeholder="Example: Bangalore"
    )

    food_preference = st.selectbox(
        "Food Preference",
        [
            "Vegetarian",
            "Non-Vegetarian",
            "Vegan"
        ]
    )

with col2:

    country = st.text_input(
        "Country",
        placeholder="Example: India"
    )

    gender = st.selectbox(
        "Gender (Optional)",
        [
            "Prefer not to say",
            "Male",
            "Female",
            "Other"
        ]
    )

    plan_type = st.selectbox(
        "Plan Type",
        [
            "Daily",
            "Weekly",
            "Monthly"
        ]
    )

st.markdown("### 🩺 Health Information")

health_conditions = st.text_area(
    "Health Conditions",
    placeholder="""
Examples:

Diabetes
PCOS
Hypertension
Asthma
Thyroid Issues
Vitamin D Deficiency

You can enter multiple conditions.
"""
)

additional_notes = st.text_area(
    "Additional Notes (Optional)",
    placeholder="""
Examples:

Night shifts
Gym-going
Food allergies
Sedentary lifestyle
Lactose intolerance
"""
)

st.markdown("---")

# ==================================
# GENERATE PLAN
# ==================================

if st.button("Generate Nutrition Plan"):

    if city.strip() == "" or health_conditions.strip() == "":
        st.warning(
            "Please enter at least City and Health Conditions."
        )

    else:

        # ==================================
        # PLAN TYPE LOGIC
        # ==================================

        if plan_type == "Daily":

            duration_instruction = """
Generate ONLY ONE DAY nutrition plan.

Do NOT generate multiple days.
"""

        elif plan_type == "Weekly":

            duration_instruction = """
Generate a COMPLETE 7-day nutrition plan.

Create separate sections:

Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday
"""

        else:

            duration_instruction = """
Generate a COMPLETE monthly nutrition plan.

Break the plan into:

Week 1
Week 2
Week 3
Week 4
"""

        prompt = f"""
You are NutriWise AI, an expert nutrition and lifestyle assistant.

USER DETAILS

Age: {age}
Gender: {gender}
City: {city}
Country: {country}
Food Preference: {food_preference}
Health Conditions: {health_conditions}
Additional Notes: {additional_notes}

TASK

Generate a highly personalized nutrition plan.

{duration_instruction}

IMPORTANT RULES

1. Do NOT begin by discussing health objectives.

2. First provide the nutrition plan.

3. Use foods commonly available in the user's city and country.

4. Consider climate and seasonal conditions.

5. Consider all health conditions carefully.

6. If multiple health conditions are provided,
prioritize recommendations that satisfy all conditions simultaneously.

7. Avoid contradictory dietary advice.

8. Keep recommendations practical and realistic.

9. Do not provide medical diagnosis.

10. Use professional but easy-to-understand language.

OUTPUT FORMAT

# Personalized Nutrition Plan

## Breakfast

## Mid-Morning Snack

## Lunch

## Evening Snack

## Dinner

------------------------------------------------

# Foods to Prioritize

Explain why these foods are beneficial.

------------------------------------------------

# Foods to Avoid

Explain why these foods should be avoided.

------------------------------------------------

# Hydration Guidance

Provide water intake recommendations and hydration tips.

------------------------------------------------

# Lifestyle Recommendations

Include:

- Walking
- Exercise
- Sleep habits
- Stress management
- Meal timing

------------------------------------------------

# Why These Recommendations Were Chosen

Explain how the recommendations address the user's health conditions.

------------------------------------------------

# Expected Health Benefits

Explain possible positive outcomes.

Examples:

- Better blood sugar control
- Improved energy levels
- Better digestion
- Better heart health
- Improved hormonal balance
- Weight management

Do NOT guarantee results.

------------------------------------------------

# Environmental & Climate Considerations

Provide city-specific recommendations.

Consider:

- Climate
- Seasonal conditions
- Urban pollution exposure
- Air quality
- Heat
- Humidity
- Respiratory health

If relevant, suggest:

- Antioxidant-rich foods
- Hydration strategies
- Outdoor activity precautions

------------------------------------------------

End with a short motivational message.
"""

        with st.spinner(
            "Generating your personalized nutrition plan..."
        ):

            try:

                response = model.generate_content(prompt)

                st.success(
                    "Nutrition Plan Generated Successfully!"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Plan Type", plan_type)

                with col2:
                    st.metric("City", city)

                with col3:
                    st.metric(
                        "Conditions",
                        len(
                            [x for x in health_conditions.split(",")
                             if x.strip()]
                        )
                    )

                with st.expander(
                    "📋 View Nutrition Plan",
                    expanded=True
                ):
                    st.markdown(response.text)

                    st.download_button(
                        label="📄 Download Nutrition Plan",
                        data=response.text,
                        file_name="NutriWise_Plan.txt",
                        mime="text/plain"
                    )

            except Exception as e:

                st.error("An error occurred.")

                st.code(str(e))

                st.markdown("---")

st.caption(
    "NutriWise AI • Powered by Google Gemini • Gen AI Academy APAC"
)