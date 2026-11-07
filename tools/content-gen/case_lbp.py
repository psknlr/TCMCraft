"""Case tcm-sg-lbp-01 — recurrent low back pain at a fictional Singapore community TCM clinic.

The first complete TCMCraft episode (docs/DESIGN.md §7, roadmap phase 1): consultation, the four
examinations, disease and pattern assessment, a prescription that the dispensary queries and the
prescriber revises as a new version, a first acupuncture session, and a one-week review that has to
separate incomplete adherence from a wrong assessment.

Synthetic: no real patient, no source report. Clinical statements follow the guidance named in
`provenance.review.guidelines`; what could not be verified is listed under "To verify" in the README.
"""

from __future__ import annotations

from common import KW, L

CASE_ID = "tcm-sg-lbp-01"

PHASES_EARLY = ["consult", "treatment"]
FOLLOWUP = ["followup"]

AUTHORED = L("虚构教学病例：由编者撰写。", "Fictional teaching case: authored.")


def hx(id, topic, q, a, kw, *, disclosure="on-ask", required=False, phases=None, exclude=None, safety=None, supersedes=None):
    item = {"id": id, "topic": topic, "question": q, "answer": a, "keywords": kw, "disclosure": disclosure}
    if exclude:
        item["excludeKeywords"] = exclude
    if safety:
        item["safety"] = safety
    if required:
        item["required"] = True
    if phases:
        item["phases"] = phases
    if supersedes:
        item["supersedes"] = supersedes
    item["source"] = AUTHORED
    return item


# ---------------------------------------------------------------------------------------------
# History (inquiry · 问诊)
# ---------------------------------------------------------------------------------------------

HISTORY = [
    hx(
        "h-presenting", "presenting-complaint",
        L("今天哪里不舒服，怎么来看了？", "What brings you in today?"),
        L("腰又痛起来了，这次差不多三个星期，比以前几次都难受，所以想来看看中医。",
          "My lower back's aching again — about three weeks this time, and worse than the other times, so I thought I'd try TCM."),
        KW(["哪里不舒服", "来看什么", "怎么来看", "主要问题", "什么问题", "这次多久", "痛了多久", "今天来"],
           ["whatbringsyou", "main problem", "the trouble", "how long this time", "whatsthematter", "trouble today", "reason for visit"]),
        disclosure="volunteer", required=True, phases=PHASES_EARLY,
    ),
    hx(
        "h-onset", "hpi",
        L("这次是怎么开始的？以前也这样痛过吗？", "How did this episode start, and has it happened before?"),
        L("三个星期前帮我妈妈搬一个柜子，第二天早上就开始痛。其实三年前第一次痛，之后一年发两三次，每次贴膏药两到四个星期就好。",
          "Three weeks ago I helped my mum shift a cupboard, and the next morning it started. The first time was three years ago — since then it comes two or three times a year, and each time it settles in two to four weeks with plasters."),
        KW(["怎么开始", "什么诱因", "以前痛过", "第一次痛", "发作过", "反复发作", "搬重物", "扭到"],
           ["start", "began", "previous episodes", "happened before", "first time", "trigger", "lifting", "howitstarted"]),
    ),
    hx(
        "h-site", "pain",
        L("具体痛在哪里？会不会往别的地方放射？", "Where exactly is the pain, and does it spread anywhere?"),
        L("就是腰下面这一圈，两边都痛，右边更明显。有时候会窜到右边屁股，但不会过膝盖。",
          "Right across the low back, both sides, more on the right. Sometimes it goes into my right buttock, but never past the knee."),
        KW(["痛在哪", "哪个位置", "具体位置", "放射", "窜到", "往下走", "哪一边", "臀部"],
           ["whereisthepain", "wheredoesithurt", "spread", "radiate", "radiation", "buttock", "leg pain", "which side"]),
        required=True, phases=PHASES_EARLY,
    ),
    hx(
        "h-character", "pain",
        L("是什么样的痛？早上起来会不会僵？", "What does the pain feel like, and are you stiff in the mornings?"),
        L("是一种沉沉的酸痛，像背着一包湿沙一样。早上起床腰很僵，要活动半个钟头左右才松开。",
          "A heavy, dull ache — like carrying a bag of wet sand. In the morning my back is stiff, and it takes about half an hour of moving around to loosen up."),
        KW(["什么样的痛", "怎么个痛法", "痛的性质", "酸痛", "刺痛", "胀痛", "晨僵", "早上僵"],
           ["itfeellike", "kind of pain", "describe the pain", "sharp", "dull", "stiff", "morning stiffness", "character"]),
        phases=PHASES_EARLY,
    ),
    hx(
        "h-modifiers", "pain",
        L("什么情况下会加重，什么能让它好一点？", "What makes it worse, and what eases it?"),
        L("在公司冷气房里坐久了最惨，下雨天也比较痛。洗个热水澡、起来走一走、贴个暖贴就舒服一点。",
          "Sitting for a long time in the freezing air-con at work is the worst, and rainy days are worse too. A hot shower, walking around or a heat patch makes it better."),
        KW(["加重", "什么时候更痛", "缓解", "舒服些", "减轻", "天气", "热敷", "吹冷气"],
           ["worse", "better", "eases", "relieve", "aggravate", "weather", "heat", "rainy days", "air con"]),
        required=True, phases=PHASES_EARLY,
    ),
    hx(
        "h-severity", "pain",
        L("如果0分是不痛、10分是最痛，现在大概几分？", "If 0 is no pain and 10 the worst imaginable, how bad is it now?"),
        L("平时大概六分。晚上翻身的时候会痛醒。", "About a six most of the day. Turning over in bed wakes me up."),
        KW(["几分", "多痛", "疼痛评分", "严重程度", "痛得厉害吗", "零到十"],
           ["how bad", "severity", "pain score", "outoften", "outof10", "rate the pain"]),
        phases=PHASES_EARLY,
    ),
    hx(
        "h-redflag-neuro", "ros",
        L("腿脚有没有麻木、刺痛或者没力气？", "Any numbness, tingling or weakness in your legs or feet?"),
        L("没有，腿脚都不麻，也没有没力气，走路、上楼梯都正常。",
          "No — no numbness or pins and needles, no weakness. Walking and stairs are fine."),
        KW(["麻木", "发麻", "刺痛感", "没力气", "无力", "脚麻", "针刺感", "下肢感觉"],
           ["numb", "numbness", "tingling", "pins and needles", "weakness", "weak legs", "foot drop", "sensation"]),
        required=True, phases=PHASES_EARLY,
    ),
    hx(
        "h-redflag-ce", "ros",
        L("小便、大便控制得住吗？两腿之间、肛门周围有没有发麻？",
          "Any trouble controlling your bladder or bowels, or numbness between your legs or around the back passage?"),
        L("没有，大小便都控制得住，也没有解不出来，下面也没有麻的感觉。",
          "No — I've no trouble holding my water or my bowels, no trouble going, and no numbness down there."),
        KW(["大小便能控制", "控制大小便", "大小便失禁", "控制不住", "控制得住", "会阴", "马鞍区", "肛门周围", "尿不出", "排尿困难"],
           ["bladder", "incontinence", "saddle", "perineum", "retention", "back passage", "control your bowels", "bowel control"]),
        required=True, phases=PHASES_EARLY,
        exclude=KW(["颜色", "夜尿", "起夜", "大便稀", "成形"], ["colour", "nocturia", "loose", "consistency", "formed"]),
        safety={"datum": "cauda-equina", "finding": "negative"},
    ),
    hx(
        "h-redflag-systemic", "ros",
        L("最近有没有发烧、体重莫名下降、晚上躺着休息也痛？以前得过癌症吗？",
          "Any fever, unexplained weight loss or pain at night that rest doesn't ease? Have you ever had cancer?"),
        L("没有发烧，体重也没掉。躺下休息会好一点，只是翻身的时候会痛醒。从来没得过癌症，也没长期吃过类固醇。",
          "No fever, no weight loss. Lying down rests it — it's only turning over that wakes me. Never had cancer, and I've never been on steroids for long."),
        KW(["发烧", "发热", "体重下降", "消瘦", "夜间痛", "癌症", "肿瘤", "类固醇", "盗汗"],
           ["fever", "weight loss", "cancer", "tumour", "night pain", "steroids", "red flags", "redflags", "night sweats"]),
        required=True,
    ),
    hx(
        "h-trauma", "hpi",
        L("有没有摔倒或者受过外伤？", "Have you had a fall or any injury to your back?"),
        L("没有摔，也没撞到，就是那次搬柜子。", "No fall, no knocks — just that cupboard."),
        KW(["摔倒", "跌倒", "外伤", "受伤", "撞到", "车祸"], ["fall", "fell", "injury", "injured", "trauma", "accident"]),
    ),
    hx(
        "h-coldheat", "associated-symptoms",
        L("平时怕冷还是怕热？喜欢喝冷的还是热的？", "Do you feel the cold or the heat more, and do you prefer hot or cold drinks?"),
        L("我比较怕冷，尤其腰和膝盖，冷气一吹就不舒服。喜欢喝热的，冰的我不太敢喝。不会觉得身上发热。",
          "I feel the cold more, especially in my back and knees — the air-con really gets to me. I like hot drinks; I steer clear of iced ones. I don't feel hot or feverish."),
        KW(["怕冷", "怕热", "寒热", "冷热", "喜热饮", "喜冷饮", "手脚冰凉", "畏寒"],
           ["feel the cold", "feelthecold", "feel hot", "hot or cold", "chilly", "hot drinks", "iced drinks", "prefer warm"]),
        exclude=KW(["发烧", "来之前"], ["fever", "just before"]),
    ),
    hx(
        "h-knees-fatigue", "associated-symptoms",
        L("膝盖有没有酸软？平时容易累吗？", "Do your knees feel sore and weak, and do you tire easily?"),
        L("膝盖站久了会酸酸软软的。下午三四点就觉得很累。",
          "My knees go sore and wobbly if I stand for long. By mid-afternoon I'm worn out."),
        KW(["腰膝酸软", "膝盖酸", "膝盖软", "容易累", "疲劳", "乏力", "没精神"],
           ["knees", "sore knees", "tired", "tire easily", "fatigue", "energy", "worn out"]),
        exclude=KW(["麻木", "麻"], ["numb", "tingling"]),
    ),
    hx(
        "h-urine-stool", "associated-symptoms",
        L("小便颜色怎么样，晚上要起夜吗？大便成形吗？", "What is your urine like, do you get up at night to pass water, and are your stools formed?"),
        L("小便清清的，晚上起来一次。大便偏软，喝了冰的东西有时候会拉稀。",
          "Urine's clear; I get up once at night. Stools are on the soft side, sometimes loose after iced drinks."),
        KW(["小便颜色", "尿色", "夜尿", "起夜", "大便怎么样", "大便稀", "大便成形", "二便"],
           ["urine colour", "nocturia", "getupatnight", "stools", "loose", "consistency", "bowel habit", "pass water"]),
        exclude=KW(["失禁", "控制", "会阴", "麻"], ["incontinen", "control", "saddle", "numb"]),
    ),
    hx(
        "h-sleep", "associated-symptoms",
        L("睡眠怎么样？", "How are you sleeping?"),
        L("大概睡六个钟头，翻身的时候腰痛会醒。", "About six hours. The pain wakes me when I turn over."),
        KW(["睡眠", "睡得好", "睡觉", "失眠", "睡不着", "睡几个钟头"], ["sleep", "sleeping", "insomnia", "wakeupatnight"]),
    ),
    hx(
        "h-appetite", "associated-symptoms",
        L("胃口怎么样，会口渴吗？", "How is your appetite, and are you thirsty?"),
        L("胃口还可以，不怎么口渴。", "Appetite's fine, and I'm not particularly thirsty."),
        KW(["胃口", "食欲", "口渴", "口干", "饭量"], ["appetite", "thirst", "thirsty", "dry mouth", "eating well"]),
    ),
    hx(
        "h-food-before", "other",
        L("来之前吃过或喝过什么吗？", "Did you eat or drink anything just before you came in?"),
        L("在楼下咖啡店喝了一杯咖啡，加炼奶的，还吃了两片咖椰吐司，大概二十分钟前。",
          "A kopi — with condensed milk — and two slices of kaya toast at the coffee shop downstairs, maybe twenty minutes ago."),
        KW(["来之前", "吃过什么", "喝过什么", "喝了什么", "刚刚吃", "咖啡", "喝茶", "吃早餐"],
           ["just before", "before you came", "eat", "eaten", "breakfast", "coffee", "tea", "drinkanything"]),
        disclosure="specific",
        exclude=KW(["酒", "冷的", "热的"], ["alcohol", "beer", "iced", "hot drinks"]),
    ),
    hx(
        "h-pmh", "pmh",
        L("以前有什么病吗？有没有住过院、做过手术？", "What medical problems have you had in the past — any hospital stays or operations?"),
        L("有高血压六年，胆固醇也高。四年前胸口痛，心脏放了一个支架，之后都还好，每年回心脏专科复诊一次。没做过别的手术。",
          "Blood pressure for six years, and high cholesterol. Four years ago I had chest pain and they put a stent in my heart; I've been fine since and see the heart specialist once a year. No other operations."),
        KW(["以前有什么病", "既往病史", "慢性病", "高血压", "心脏病", "住过院", "做过手术", "身体有什么病"],
           ["past medical", "medical history", "medicalhistory", "conditions", "illnesses", "operations", "surgery", "heart problems"]),
        required=True,
        exclude=KW(["家里", "家族", "爸爸", "妈妈"], ["family", "father", "mother", "parents"]),
    ),
    hx(
        "h-meds", "medications",
        L("现在在吃什么药？", "What medicines are you taking at the moment?"),
        L("早上一粒降血压的，氨氯地平5毫克；晚上一粒降胆固醇的，阿托伐他汀20毫克。腰痛就去药房买膏药贴。",
          "A blood-pressure pill in the morning — amlodipine 5 mg — and a cholesterol one at night, atorvastatin 20 mg. For the back I buy medicated plasters from the pharmacy."),
        KW(["吃什么药", "哪些药", "在吃的药", "吃的药", "用药", "药物", "长期吃药", "西药"],
           ["medicines", "medications", "tablets", "pills", "prescriptions", "regular meds"]),
        required=True,
        exclude=KW(["过敏", "阿司匹林", "抗凝", "抗血小板", "血稀", "中药", "草药", "保健品", "补品", "颗粒", "冲剂", "药包"],
                   ["allerg", "aspirin", "thinner", "thinning", "anticoag", "antiplatelet", "herbal", "supplement", "tonic", "sachet", "granule"]),
    ),
    hx(
        "h-antithrombotic", "medications",
        L("有没有吃阿司匹林或者其他抗血小板、抗凝的药？", "Do you take aspirin or any other blood-thinning medicine?"),
        L("啊，对，有一粒小小的阿司匹林，100毫克，每天早上吃，放支架以后就一直吃。我刚才忘了说，以为那算是心脏的一部分。",
          "Oh — yes, the small aspirin, 100 milligrams every morning, ever since the stent. Sorry, I forgot; I think of it as part of the heart thing."),
        KW(["阿司匹林", "抗凝", "抗血小板", "血稀", "稀血", "华法林", "氯吡格雷", "血液稀释"],
           ["aspirin", "blood thinner", "bloodthinner", "blood thinning", "anticoagulant", "antiplatelet", "warfarin", "clopidogrel"]),
        disclosure="specific", safety={"datum": "antithrombotic", "finding": "positive"},
    ),
    hx(
        "h-herbs-supplements", "medications",
        L("最近有没有吃中药、保健品或者补品？", "Are you taking any herbal remedies, supplements or tonics?"),
        L("现在没有。以前偶尔吃鱼油，这几个月都没吃了。", "Not at the moment. I used to take fish oil now and then, but not for months."),
        KW(["中药", "草药", "保健品", "补品", "鱼油", "凉茶", "维他命"],
           ["herbal", "herbs", "supplements", "tonic", "vitamins", "fish oil", "traditional medicine"]),
    ),
    hx(
        "h-allergies", "allergies",
        L("对什么药物或者食物过敏吗？", "Are you allergic to any medicines or foods?"),
        L("没有，西药没有过敏，以前吃中药也没有出过问题。", "No — no allergies to any medicine, and herbs have never given me trouble."),
        KW(["过敏", "过敏史", "药物过敏", "起疹子"], ["allergy", "allergies", "allergic", "reaction to medicine"]),
        required=True, safety={"datum": "allergy", "finding": "negative"},
    ),
    hx(
        "h-prior-acu", "other",
        L("以前针灸过吗？当时有没有不舒服？", "Have you had acupuncture before, and did anything go wrong?"),
        L("两年前在别的诊所扎过一次，坐着扎的。扎到一半我头晕、出冷汗，差点晕过去，他们马上拔针让我躺下，过一会就好了。那天我没吃早餐。",
          "Once, two years ago, at another clinic — sitting up. Halfway through I went giddy and broke into a cold sweat, nearly fainted; they took the needles out and laid me down, and I was fine after a while. I hadn't had breakfast that day."),
        KW(["针灸过", "扎过针", "以前针灸", "晕针", "针灸的经验", "拔罐", "刮痧"],
           ["acupuncture before", "needles before", "previous acupuncture", "fainted", "fainting", "cupping", "tried acupuncture"]),
        disclosure="specific", safety={"datum": "needle-syncope", "finding": "positive"},
    ),
    hx(
        "h-occupation", "social",
        L("你做什么工作？", "What do you do for work?"),
        L("我在物流公司当运营主管，大部分时间坐在控制室看屏幕，冷气很强；有时候也要搬东西。每个星期大概上两个夜班。",
          "I'm an operations supervisor at a logistics company — mostly sitting in the control room watching screens, with very strong air-con, and sometimes I lift things. About two night shifts a week."),
        KW(["做什么工作", "职业", "做什么的", "上班", "夜班", "工作环境"], ["job", "occupation", "foraliving", "shifts", "employer", "work as"]),
        exclude=KW(["影响", "还能"], ["affect", "manage"]),
    ),
    hx(
        "h-living", "social",
        L("家里跟谁住？", "Who do you live with at home?"),
        L("跟太太和两个孩子住组屋，有电梯。我妈妈住在附近。", "With my wife and our two teenagers in an HDB flat — there's a lift. My mum lives nearby."),
        KW(["跟谁住", "住在哪", "家里几个人", "组屋", "住的地方"], ["livewith", "livingwith", "household", "whoisathome", "housing"]),
    ),
    hx(
        "h-smoking-alcohol", "social",
        L("抽烟喝酒吗？", "Do you smoke or drink alcohol?"),
        L("放支架以后就戒烟了。周末偶尔喝一两罐啤酒。", "I stopped smoking after the stent. A can or two of beer at weekends, sometimes."),
        KW(["抽烟", "吸烟", "喝酒", "饮酒", "啤酒", "烟酒"], ["smoke", "smoking", "cigarettes", "alcohol", "beer"]),
        exclude=KW(["咖啡", "来之前"], ["coffee", "just before"]),
    ),
    hx(
        "h-exercise", "functional",
        L("平时有运动吗？", "Do you exercise regularly?"),
        L("没有固定运动。以前会跑步，这几年没跑了，周末偶尔散散步。", "Nothing regular. I used to jog, but not for years; I go for a walk at weekends sometimes."),
        KW(["运动", "锻炼", "跑步", "散步", "健身"], ["exercise", "sport", "jogging", "gym", "physical activity"]),
    ),
    hx(
        "h-function", "functional",
        L("腰痛对日常生活和工作影响有多大？", "How much is the back affecting your daily life and work?"),
        L("工作还能做，但不敢搬重的。早上穿袜子很辛苦。走路半个钟头没问题。",
          "I can still work, but I don't dare lift anything heavy. Putting on socks in the morning is a struggle. I can walk half an hour fine."),
        KW(["影响", "日常生活", "生活自理", "穿袜子", "还能上班", "能走多久"], ["daily life", "affecting", "function", "daytoday", "cope", "manage at work"]),
    ),
    hx(
        "h-family", "family",
        L("家里人有什么病吗？", "Does anything run in your family?"),
        L("我爸爸老了以后腰也不好。其他的我不太清楚。", "My father had a bad back when he got older. Nothing else I know of."),
        KW(["家族史", "家里人", "父母", "遗传", "家人有什么病"], ["family history", "familyhistory", "run in the family", "parents", "inherited"]),
    ),
    hx(
        "h-ice", "ice",
        L("你自己担心是什么问题？希望这次看诊能帮到什么？", "What are you worried this might be, and what are you hoping for from today?"),
        L("我怕是椎间盘突出，要开刀。我希望能继续上班，西药能少吃就少吃。还有，中药会不会跟我的心脏药冲突？",
          "I'm scared it's a slipped disc and I'll need an operation. I want to keep working, and I'd rather not take more Western pills. And — will herbs clash with my heart medicines?"),
        KW(["担心", "顾虑", "希望", "期望", "最怕", "有什么想法", "想达到"], ["worried", "worry", "concerns", "hoping", "expectations", "ideas", "afraid"]),
        required=True,
    ),
    hx(
        "h-language", "other",
        L("你习惯用华语还是英语沟通？药袋上的说明看得懂吗？", "Which language do you prefer, Mandarin or English, and can you read the medicine labels?"),
        L("华语英语都可以，华语比较自在。中文英文的标签我都看得懂。", "Either is fine; Mandarin is more comfortable. I can read labels in English and Chinese."),
        KW(["华语", "英语", "语言", "翻译", "看得懂", "中文"], ["language", "mandarin", "english", "interpreter", "translate", "read labels"]),
    ),
    hx(
        "h-blood-tests", "pmh",
        L("最近有没有验过血，肝肾功能怎么样？", "Have you had any recent blood tests — kidney or liver function?"),
        L("去年综合诊所有抽血，结果我不清楚，他们没跟我说什么。", "The polyclinic took blood last year, but I don't know the results — they didn't tell me anything about them."),
        KW(["验血", "抽血", "血液检查", "肝功能", "肾功能", "化验"], ["blood test", "bloods", "kidney function", "liver function", "lab tests"]),
        disclosure="unknown",
    ),
    hx(
        "h-bruising", "pmh",
        L("平时容易瘀青或出血吗？", "Do you bruise or bleed easily?"),
        L("不算吧，这几年好像比较容易瘀青一点。没有流血，大便也没有黑的。",
          "Not really — maybe I bruise a little more easily these few years. No bleeding, and no black stools."),
        KW(["瘀青", "淤青", "容易出血", "流血", "黑便", "牙龈出血"], ["bruise", "bruising", "bleed easily", "bleeding", "black stools", "gums"]),
        phases=PHASES_EARLY,
    ),
    # --- one week later (phase twins of the present-tense items) ---------------------------------
    hx(
        "h-fu-status", "hpi",
        L("这一个星期腰怎么样了？", "How has your back been this past week?"),
        L("好一些。针灸完那两三天松了很多，现在大概四分；可是上完夜班又僵回来，早上僵十五分钟左右。",
          "Better. For two or three days after the needles it was much looser — it's about a four now. But after night shift it stiffens up again; mornings are stiff for about fifteen minutes."),
        KW(["这个星期", "这一周", "这周", "好点了吗", "好一点", "有没有好转", "上次以后"],
           ["this week", "past week", "improved", "any better", "progress", "since last time"]),
        phases=FOLLOWUP, supersedes=["h-presenting", "h-severity", "h-character"],
    ),
    hx(
        "h-fu-adherence", "medications",
        L("颗粒冲剂有没有按时吃？", "Have you been taking the granules as we agreed?"),
        L("早上那包每天都有吃。晚上那包常常忘，上夜班那两晚没吃，还有三个晚上忘了。药有点苦，但还能接受。",
          "The morning sachet, every day. The evening one I often missed — the two night-shift evenings, and three other nights I just forgot. It's a bit bitter, but bearable."),
        KW(["按时吃", "有没有吃药", "颗粒", "冲剂", "漏吃", "忘了吃", "吃了几包", "中药吃了吗"],
           ["granules", "sachets", "taking the herbs", "missed doses", "missed any", "adherence", "remember to take"]),
        required=True, phases=FOLLOWUP,
    ),
    hx(
        "h-fu-exercise", "functional",
        L("运动和坐姿方面的建议有做到吗？", "How did you get on with the exercises and the advice about sitting?"),
        L("头三天有做伸展，后来忙就停了。控制室还是一坐好几个钟头，冷气很冷，我也没带外套。",
          "I did the stretches for the first three days, then got busy and stopped. Still sitting for hours in the control room — the air-con is freezing and I didn't bring a jacket."),
        KW(["伸展", "运动做了吗", "练习", "坐姿", "起来活动", "外套"], ["exercises", "stretches", "stretching", "sitting breaks", "the advice", "jacket"]),
        phases=FOLLOWUP,
    ),
    hx(
        "h-fu-adverse", "other",
        L("治疗以后有没有什么不舒服或者副作用？", "Any side effects or problems since the treatment?"),
        L("右边膝盖后面扎针的地方有一点点瘀青，现在不痛了。没有头晕，胃也没有不舒服，没有出血，大便颜色正常。",
          "A tiny bruise behind my right knee where a needle went in — it doesn't hurt now. No giddiness, no stomach upset, no bleeding, and my stools are a normal colour."),
        KW(["副作用", "不良反应", "治疗以后", "胃不舒服", "头晕", "针以后"],
           ["side effects", "sideeffects", "problems since", "upset stomach", "giddy", "since the treatment"]),
        required=True, phases=FOLLOWUP, supersedes=["h-bruising"],
    ),
    hx(
        "h-fu-redflags", "ros",
        L("现在腿脚有没有麻木无力？大小便正常吗？", "Any numbness or weakness in your legs now, and are your bladder and bowels normal?"),
        L("都没有，腿不麻，也有力气，大小便都正常。", "None of that — my legs are fine, no numbness, and everything's normal down below."),
        KW(["现在腿", "现在大小便", "现在有没有麻", "新的麻木"], ["new weakness", "new numbness", "newnumbness", "still no numbness"]),
        required=True, phases=FOLLOWUP, supersedes=["h-redflag-neuro", "h-redflag-ce"],
    ),
    hx(
        "h-fu-other-care", "medications",
        L("这一周有没有看别的医生，或者开始吃新的药？", "Have you seen any other doctor or started anything new this week?"),
        L("没有。照样吃我那三粒药，阿司匹林也每天吃。", "No. Same three pills as always, the aspirin included, every day."),
        KW(["别的医生", "看过医生", "新的药", "其他治疗", "别的药"], ["other doctor", "newmedicine", "startedanything", "other treatment", "seen anyone"]),
        phases=FOLLOWUP,
    ),
]


# ---------------------------------------------------------------------------------------------
# Examination (inspection · listening and smelling · palpation, plus the biomedical screen)
# ---------------------------------------------------------------------------------------------

def ex(id, system, maneuver, finding, kw, *, abnormal=False, required=False, phases=PHASES_EARLY, requires=None, exclude=None):
    item = {"id": id, "system": system, "maneuver": maneuver, "keywords": kw, "finding": finding, "abnormal": abnormal}
    if exclude:
        item["excludeKeywords"] = exclude
    if requires:
        item["requires"] = requires
    if required:
        item["required"] = True
    item["phases"] = phases
    item["source"] = AUTHORED
    return item


EXAM = [
    ex("e-general", "general",
       L("望神色形态：观察精神、面色、体型与步态", "Inspect spirit, complexion, build and gait"),
       L("神清，精神可；面色略淡少华；体型偏胖；行走时腰部略僵，弯腰谨慎，坐下时用手撑扶椅子。",
         "Alert and engaged; complexion slightly pale and lustreless; heavy-set; walks with a slightly stiff lower back, bends cautiously and pushes on the chair arms to sit."),
       KW(["望诊", "望神", "面色", "步态", "体型", "一般情况"], ["inspect", "inspection", "general appearance", "gait", "complexion", "lookathim"]),
       abnormal=True, required=True),
    ex("e-vitals", "vitals",
       L("测量血压、脉率、体温和体重", "Measure blood pressure, pulse rate, temperature and weight"),
       L("血压136/84 mmHg，脉率72次/分、齐，体温36.6℃，呼吸14次/分；体重78 kg，身高170 cm（BMI 27.0）。",
         "Blood pressure 136/84 mmHg, pulse 72/min and regular, temperature 36.6 °C, respiratory rate 14/min; weight 78 kg, height 170 cm (BMI 27.0)."),
       KW(["生命体征", "血压", "体温", "体重", "测量"], ["vital signs", "vitals", "blood pressure", "temperature", "weight", "bmi"])),
    ex("e-voice-odour", "general",
       L("闻诊：听声音与呼吸，嗅气味", "Listening and smelling: voice, breathing and odour"),
       L("语声清晰，音量正常；呼吸平顺，无咳嗽；口中有咖啡味，无特殊体味。",
         "Voice clear and of normal strength; breathing quiet and even, no cough; coffee on his breath, no unusual body odour."),
       KW(["闻诊", "听声音", "嗅气味", "气味", "口气", "呼吸声"], ["listen", "listening", "smell", "odour", "voice", "breath"]),
       required=True),
    ex("e-tongue", "heent",
       L("望舌：请患者漱口后，在自然光下直接观察舌质与舌苔", "Inspect the tongue directly in daylight after he rinses his mouth"),
       L("舌质淡，舌体稍胖大，边有齿痕；苔薄白腻，润；漱口后舌面无染色；舌下络脉无明显迂曲。",
         "Tongue body pale and slightly enlarged with tooth marks along the edges; coating thin, white and greasy, moist; no staining once rinsed; sublingual veins not distended."),
       KW(["舌", "舌象", "舌苔", "舌质", "看舌头", "伸舌头", "望舌"], ["tongue", "coating", "inspect the tongue", "stick out"]),
       abnormal=True, required=True),
    ex("e-pulse", "cardiovascular",
       L("切脉：寸关尺三部，浮中沉取", "Take the radial pulse at cun, guan and chi with light, medium and deep pressure"),
       L("脉沉细，两尺脉弱；脉率约72次/分，节律齐。", "Pulse deep and thready, weakest at both chi positions; rate about 72/min, regular."),
       KW(["切脉", "把脉", "号脉", "脉象", "摸脉", "诊脉"], ["pulse", "radial pulse", "pulse diagnosis", "feel the pulse", "take the pulse"]),
       abnormal=True, required=True),
    ex("e-lumbar-palp", "musculoskeletal",
       L("腰部望诊与触诊：棘突、椎旁肌与皮温", "Inspect and palpate the lumbar spine, paraspinal muscles and skin temperature"),
       L("L3–S1两侧椎旁肌紧张、压痛，右侧明显；棘突无压痛、无叩击痛；腰部皮温偏凉，无红肿。",
         "Paravertebral muscles tense and tender on both sides from L3 to S1, right more than left; no spinous-process tenderness or percussion pain; skin of the lower back cool to touch, no swelling or redness."),
       KW(["触诊腰部", "按压腰", "腰部压痛", "摸腰", "按诊", "叩击痛"], ["palpate", "palpation", "tenderness", "press on", "spinal tenderness", "lumbar exam"]),
       abnormal=True, required=True),
    ex("e-lumbar-rom", "musculoskeletal",
       L("检查腰椎活动度", "Check lumbar range of movement"),
       L("前屈受限，指尖仅达小腿中段并诱发酸痛；后伸轻度痛；右侧屈稍受限。",
         "Forward flexion limited — fingertips to mid-shin, reproducing the ache; extension mildly painful; side flexion to the right slightly reduced."),
       KW(["活动度", "弯腰", "前屈", "后伸", "侧弯", "转腰"], ["range of movement", "range of motion", "bend forward", "flexion", "extension"]),
       abnormal=True),
    ex("e-slr", "neurological",
       L("直腿抬高试验与坐位屈颈（slump）试验", "Straight-leg raise and slump test"),
       L("直腿抬高试验双侧均达80°，仅在终末有腰部牵拉感，无下肢放射痛；slump试验阴性。",
         "Straight-leg raise to 80° on both sides with only a pulling feeling in the low back at the end of range, no leg pain; slump test negative."),
       KW(["直腿抬高", "抬腿试验", "神经牵拉", "坐位屈颈"], ["straight leg raise", "straightlegraise", "slr", "slump", "nerve tension", "lasegue"]),
       required=True),
    ex("e-neuro", "neurological",
       L("双下肢神经系统检查", "Neurological examination of the lower limbs"),
       L("双下肢肌力5级（包括踝背屈与拇背伸）；膝、踝反射对称存在；轻触觉正常，包括会阴区（询问及检查所及）；足跟、足尖行走正常。",
         "Lower-limb power 5/5 including ankle dorsiflexion and great-toe extension; knee and ankle reflexes present and symmetrical; light touch normal, including the saddle area as tested; heel and toe walking normal."),
       KW(["神经系统", "肌力", "反射", "感觉检查", "下肢神经", "腱反射"], ["neuro", "neurological", "power", "reflexes", "sensation", "myotomes", "dermatomes"]),
       required=True, requires=["reflex-hammer"]),
    ex("e-hips", "musculoskeletal",
       L("检查双髋关节", "Examine both hips"),
       L("双髋屈曲及内外旋活动完全，无痛。", "Hip flexion and rotation full and painless on both sides."),
       KW(["髋关节", "髋部", "转髋", "4字试验"], ["hip", "hips", "hip rotation", "faber"])),
    ex("e-abdomen", "abdomen",
       L("腹部触诊", "Palpate the abdomen"),
       L("腹软，无压痛，未触及搏动性包块。", "Soft and non-tender; no pulsatile mass."),
       KW(["腹部", "摸肚子", "腹部触诊", "肚子"], ["abdomen", "abdominal", "tummy", "belly"])),
    ex("e-skin-back", "skin",
       L("检查腰背部皮肤及拟针刺部位", "Inspect the skin over the back and the planned needling sites"),
       L("腰背部皮肤完整，无皮疹、破损、感染或水疱；左侧腰部有一处陈旧小色素斑。",
         "Skin over the back intact — no rash, broken skin, infection or blisters; a small old pigmented spot on the left flank."),
       KW(["皮肤", "背部皮肤", "皮疹", "针刺部位"], ["skin", "rash", "skin of the back", "needling sites"])),
    # --- one week later ----------------------------------------------------------------------
    ex("e-fu-lumbar", "musculoskeletal",
       L("复查腰部压痛与活动度", "Re-examine lumbar tenderness and range of movement"),
       L("椎旁压痛减轻，现主要在右侧L4–S1；前屈改善，指尖达踝部；后伸无痛；腰部皮温仍偏凉。",
         "Paravertebral tenderness milder, now mainly right L4–S1; flexion improved to fingertips at the ankles; extension pain-free; the lower back still cool to touch."),
       KW(["复查腰部", "腰部压痛", "活动度", "弯腰", "触诊腰部"], ["re-examine the back", "tenderness", "range of movement", "bend forward", "palpate"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-sites", "skin",
       L("查看上次针刺部位", "Inspect last week's needling sites"),
       L("右侧腘窝（委中穴处）有一处约1 cm的淡黄绿色瘀斑，无压痛、无肿胀或包块；其余针刺部位正常。",
         "A faint 1 cm yellow-green bruise in the right popliteal fossa at the BL40 (Weizhong) site, non-tender, no swelling or lump; other sites clear."),
       KW(["针刺部位", "针眼", "瘀斑", "膝盖后面", "皮肤"], ["needling sites", "needle sites", "bruise", "behind the knee", "skin"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-neuro", "neurological",
       L("复查双下肢神经系统与直腿抬高", "Repeat the lower-limb neurological check and straight-leg raise"),
       L("肌力、反射与轻触觉均正常，与上周一致；直腿抬高双侧80°，无下肢痛。",
         "Power, reflexes and light touch normal and unchanged from last week; straight-leg raise 80° on both sides without leg pain."),
       KW(["神经系统", "肌力", "反射", "直腿抬高", "感觉"], ["neuro", "neurological", "power", "reflexes", "straight leg raise"]),
       required=True, phases=FOLLOWUP, requires=["reflex-hammer"]),
    ex("e-fu-tongue", "heent",
       L("复查舌象（漱口后、自然光下）", "Re-inspect the tongue (rinsed, in daylight)"),
       L("舌淡，稍胖大，边有齿痕；苔薄白，腻象较上周稍减。", "Pale, slightly enlarged with tooth marks; coating thin and white, a little less greasy than last week."),
       KW(["舌", "舌象", "舌苔", "望舌"], ["tongue", "coating", "inspect the tongue"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-pulse", "cardiovascular",
       L("复诊切脉", "Retake the pulse"),
       L("脉沉细，尺脉弱；70次/分，节律齐。", "Deep and thready, chi positions weak; 70/min, regular."),
       KW(["切脉", "把脉", "脉象", "号脉"], ["pulse", "radial pulse", "take the pulse"]),
       abnormal=True, phases=FOLLOWUP),
]


# ---------------------------------------------------------------------------------------------
# Investigations: records, images and what the clinic itself documents
# ---------------------------------------------------------------------------------------------

PRIOR_RECORDS = {
    "text": L(
        "患者自带的综合诊所用药清单（两个月前打印）：氨氯地平5 mg 每日一次（早）；阿托伐他汀20 mg 每日一次（晚）；阿司匹林100 mg 每日一次（早），备注“冠脉支架术后，长期服用”。药物过敏：无已知药物过敏。\n"
        "既往腰椎X线报告（两年前，综合诊所转介）：L4/5椎间隙轻度变窄，椎体前缘小骨赘；生理曲度与序列正常；未见骨折或骨质破坏。报告备注：此类退行性改变在该年龄段常见。",
        "Patient-held polyclinic medication list (printed two months ago): amlodipine 5 mg once daily (morning); atorvastatin 20 mg once daily (night); aspirin 100 mg once daily (morning), annotated \"long-term, after coronary stent\". Allergies: no known drug allergy.\n"
        "Previous lumbar spine X-ray report (two years ago, polyclinic referral): mild disc-space narrowing at L4/5 with small anterior osteophytes; normal alignment; no fracture or destructive lesion. Comment: degenerative changes of this kind are common at this age.",
    ),
    "note": L("这是患者自带的打印件，不是本诊所的记录；以患者口述核对。", "A printout the patient brought, not this clinic's record; confirm it with him."),
    "source": AUTHORED,
}

INVESTIGATIONS = [
    {
        "id": "intake-tongue-photo",
        "name": L("自助问诊机舌象照片（候诊区）", "Intake kiosk tongue photo (waiting area)"),
        "category": "record",
        "aliases": KW(["舌象照片", "舌照", "自助机", "候诊区照片", "舌象记录"], ["kiosk", "intake photo", "tongue photo", "kiosk photo", "intake questionnaire"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "useful",
        "availability": {"historical": False},
        "results": {
            "consult": {
                "date": L("今日挂号时（10:24）", "Today at registration (10:24)"),
                "text": L(
                    "自助问诊机在候诊区拍摄的舌象照片：暖色灯光下舌质偏暗红，舌中、舌根部舌苔厚，呈黄褐色。采集信息：环境为暖白光；画面内未检测到色卡；轻度运动模糊。机器质量提示：“颜色校验未通过——请在标准光源下重拍”。",
                    "Tongue photo taken by the self-service intake kiosk in the waiting area: under warm lighting the tongue body looks dull red, with a thick, yellow-brown coating over the centre and root. Capture data: warm-white ambient light; colour reference card not detected in frame; slight motion blur. Kiosk quality flag: \"Colour check failed — repeat under standard lighting\".",
                ),
                "note": L("自助机照片是候诊时由患者自行拍摄的，未经临床人员核对。", "The kiosk photo was taken by the patient himself while waiting and has not been checked by clinical staff."),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "tongue-recapture",
        "name": L("标准光源下重新采集舌象（漱口后）", "Repeat tongue image under standard lighting (after rinsing)"),
        "category": "bedside",
        "aliases": KW(["重新拍舌", "重拍舌象", "标准光源", "舌象采集仪", "再拍一次舌"], ["repeat tongue", "recapture", "retake tongue", "standard light", "tongue camera"]),
        "risk": "none",
        "performedAt": "bedside",
        "value": "useful",
        "results": {
            "consult": {
                "date": L("今日10:52", "Today, 10:52"),
                "text": L(
                    "漱口后在舌象采集仪标准环形光源下拍摄，色卡在画面内，质量校验通过：舌质淡，舌体稍胖大，边有齿痕；苔薄白腻，润；无黄苔；舌下络脉无明显迂曲。",
                    "Taken after he rinsed with water, under the tongue-imaging station's standard ring light with the colour card in frame; quality check passed: tongue body pale, slightly enlarged, with tooth marks at the edges; coating thin, white and greasy, moist; no yellow coating; sublingual veins not distended.",
                ),
                "note": L("与自助机照片相比，黄褐色已消失。", "Compared with the kiosk photo, the yellow-brown colour has gone."),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "prior-records",
        "name": L("患者自带的综合诊所用药清单及既往腰椎X线报告", "Patient-held polyclinic medication list and previous lumbar X-ray report"),
        "category": "record",
        "aliases": KW(["用药清单", "药物清单", "既往记录", "综合诊所", "旧报告", "X光报告", "以前的片子"],
                      ["medication list", "polyclinic", "previous records", "old x-ray", "x-ray report", "prior records", "printout"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "essential",
        "availability": {"historical": True},
        "results": {"consult": PRIOR_RECORDS, "treatment": PRIOR_RECORDS, "followup": PRIOR_RECORDS},
    },
    {
        "id": "dispensary-query",
        "name": L("药房对处方第1版的审方意见", "Dispensary query on prescription version 1"),
        "category": "record",
        "aliases": KW(["审方", "药房意见", "药房查询", "药房反馈", "处方审核"], ["dispensary query", "pharmacy query", "prescription review", "dispensary", "review comments"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "essential",
        "availability": {"earliestPhase": "treatment", "when": {"intervened": "rx-draft"}, "historical": False},
        "results": {
            "treatment": {
                "date": L("今日11:15", "Today, 11:15"),
                "text": L(
                    "审方人：林先生（中药调剂）。处方第1版暂缓调剂，待处方医师处理以下两点：\n"
                    "1. 库存：桑寄生配方颗粒缺货，预计周四（两天后）到货。供应商可提供槲寄生配方颗粒——这是另一味药材，在药典中单列；药房不能自行替换，需处方医师开具新版本处方。\n"
                    "2. 用药史不完整：处方“现用药物”栏只列有氨氯地平和阿托伐他汀。方中有当归、川芎（活血药）。请向患者确认是否服用抗血小板或抗凝药物，并记录在案。",
                    "Reviewer: Mr Lim (TCM dispensing). Prescription version 1 is on hold until the prescriber resolves two points:\n"
                    "1. Stock: Taxilli Herba (桑寄生) granules are out of stock until Thursday (two days). The supplier can provide Visci Herba (槲寄生) granules — a different medicinal with its own Pharmacopoeia monograph. The dispensary cannot substitute on its own; it needs a new prescription version from the prescriber.\n"
                    "2. Medication history incomplete: the prescription's current-medicines field lists amlodipine and atorvastatin only. The formula contains 当归 and 川芎 (blood-activating herbs). Please confirm with the patient whether he takes any antiplatelet or anticoagulant medicine, and record it.",
                ),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "dispensing-record",
        "name": L("调剂与发药记录", "Dispensing record"),
        "category": "record",
        "aliases": KW(["发药记录", "调剂记录", "配药记录"], ["dispensing record", "supply record", "what was dispensed"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "useful",
        "availability": {"historical": False},
        "results": {
            "followup": {
                "date": L("上周初诊当日", "Last week, on the day of the first visit"),
                "text": L(
                    "按处方医师签署的第2版处方调剂（第1版作废，未调剂）：配方颗粒14包，每次1包、每日2次、饭后温水冲服，共7天；中英文标签；批号已记录；发药时已作用药交代。用药记录已更新：加入阿司匹林100 mg 每日一次。",
                    "Filled from prescription version 2 as signed by the prescriber (version 1 cancelled, never filled): 14 sachets of concentrated granules, 1 sachet twice daily after meals dissolved in warm water, for 7 days; bilingual label; batch numbers recorded; counselling given at supply. Medication record updated: aspirin 100 mg once daily added.",
                ),
                "note": L("产品的监管分类（中成药或中药材制品）按实际产品核定；本病例中的产品为虚构。", "Each product's regulatory class (Chinese proprietary medicine or traditional medicinal material) is set by the actual product; the products in this case are fictional."),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "acupuncture-record",
        "name": L("第1次针灸治疗记录", "Acupuncture session 1 record"),
        "category": "record",
        "aliases": KW(["针灸记录", "治疗记录", "上次针灸"], ["acupuncture record", "session record", "treatment record"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "useful",
        "availability": {"historical": False},
        "results": {
            "followup": {
                "date": L("上周初诊当日", "Last week, on the day of the first visit"),
                "text": L(
                    "俯卧位，枕垫支撑；洁净针刺操作，一次性无菌针。取穴：双侧肾俞、大肠俞、委中，右侧环跳，局部阿是穴3处——进针10支，留针20分钟，出针10支，核对无误。患者诉针下酸胀，无头晕、出汗。右委中出针时少量渗血，按压1分钟止。",
                    "Prone with pillow support; clean needle technique, single-use sterile needles. Points: BL23 (Shenshu), BL25 (Dachangshu) and BL40 (Weizhong) bilaterally, GB30 (Huantiao) on the right, 3 local Ashi points — 10 needles in, retained 20 minutes, 10 needles out, count checked. Reported an aching, distending sensation at the needles; no giddiness or sweating. A small bleed at right BL40 on withdrawal, stopped with 1 minute of pressure.",
                ),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "sachet-count",
        "name": L("清点剩余颗粒药包并核对服药记录", "Count the remaining granule sachets and check his dose diary"),
        "category": "bedside",
        "aliases": KW(["清点药包", "剩余药包", "数药包", "服药记录", "服药日记"], ["count sachets", "sachet count", "remaining sachets", "pill count", "dose diary"]),
        "risk": "none",
        "performedAt": "bedside",
        "value": "essential",
        "results": {
            "followup": {
                "date": L("今日复诊", "Today's review"),
                "text": L(
                    "与患者一起清点：14包中剩余6包（服用8包）。服药记录：早上一包7天都服用；晚上一包只服用1次——两次因夜班未服，另有4个晚上忘记。",
                    "Counted with him: 6 of 14 sachets left (8 taken). Dose diary: the morning sachet taken on all 7 days; the evening sachet taken once — missed twice on night shifts and forgotten on four other evenings.",
                ),
                "note": L("患者口述“三个晚上忘了”，与药包数（漏服6次）不完全一致；以清点结果为准并与患者核对。", "He said he forgot on three evenings, which does not quite match the count (six missed doses); go by the count and talk it through with him."),
                "source": AUTHORED,
            }
        },
    },
]

ORDER_MATCHING = {
    "rules": [
        {"ifMatches": "(repeat|recapture|retake|again|standard|重新|重拍|再拍|标准)", "remove": ["intake-tongue-photo"]},
        {"ifMatches": "(kiosk|intake|自助|候诊)", "remove": ["tongue-recapture"]},
    ],
}


# ---------------------------------------------------------------------------------------------
# Interventions: prescription versions, dispensing, acupuncture steps, follow-up
# ---------------------------------------------------------------------------------------------

V2 = {"any": [{"intervened": "rx-v2-substitute", "valid": True}, {"intervened": "rx-v2-omit", "valid": True}]}

FORMULA_ZH = (
    "独活寄生汤加减（去细辛）配方颗粒，以饮片当量计（克/日）：独活9、桑寄生15、杜仲10、牛膝10、秦艽9、防风9、桂枝6、茯苓15、"
    "当归9、川芎6、白芍12、熟地黄12、党参12、炙甘草6。每日1剂分2包，每次1包，每日2次，饭后温水冲服，共7天（14包）。"
)
FORMULA_EN = (
    "Modified Du Huo Ji Sheng Tang (独活寄生汤, Asarum omitted) as concentrated granules, in crude-herb equivalents (g/day): "
    "独活 Angelicae Pubescentis Radix 9, 桑寄生 Taxilli Herba 15, 杜仲 Eucommiae Cortex 10, 牛膝 Achyranthis Bidentatae Radix 10, "
    "秦艽 Gentianae Macrophyllae Radix 9, 防风 Saposhnikoviae Radix 9, 桂枝 Cinnamomi Ramulus 6, 茯苓 Poria 15, "
    "当归 Angelicae Sinensis Radix 9, 川芎 Chuanxiong Rhizoma 6, 白芍 Paeoniae Radix Alba 12, 熟地黄 Rehmanniae Radix Praeparata 12, "
    "党参 Codonopsis Radix 12, 炙甘草 Glycyrrhizae Radix Praeparata 6. One day's dose in 2 sachets: 1 sachet twice daily after meals in warm water, for 7 days (14 sachets)."
)


def iv(id, kind, name, aliases, **fields):
    item = {"id": id, "name": name, "kind": kind, "aliases": aliases}
    item.update(fields)
    return item


INTERVENTIONS = [
    iv("explain-consent", "other",
       L("说明诊断与治疗方案（含替代方案、获益与风险），取得并记录知情同意", "Explain the assessment and plan (with alternatives, benefits and risks) and record his consent"),
       KW(["知情同意", "解释病情", "说明治疗", "签同意书", "征得同意"], ["consent", "informed consent", "explain the plan", "explain treatment", "agree to treatment"]),
       dose=L("用患者偏好的语言（华语）说明：腰痛性质与预后、针灸与中药方案、其他选择（单纯自我管理与运动、看家庭医生），可能的风险（针刺处疼痛、瘀青、晕针，中药的胃肠不适及与现用药的相互作用），并如实说明疗效证据有限、各国指南意见不一；确认理解后记录同意。",
              "In his preferred language (Mandarin): what the back pain is and its outlook, the acupuncture and herbal plan, the alternatives (self-management and exercise alone, seeing his family doctor), and the risks (needle pain, bruising, fainting; stomach upset from herbs and interactions with his medicines), saying honestly that the evidence of benefit is limited and that guidelines disagree; check understanding, then record consent."),
       scope="medical", risk="none", setFlags=["consent-recorded"],
       indicatedWhen={"decided": "d-pattern"},
       response=L("陈先生点头：“这样讲我明白了。针灸可以，但这次我要躺着扎。”同意已记录。", "Mr Tan nods: \"That's clear. Acupuncture is fine — but lying down this time.\" Consent is recorded.")),
    iv("self-management", "other",
       L("自我管理建议：保持活动、循序渐进运动、腰部保暖，工作时定时起身", "Self-management advice: stay active, graded exercise, keep the back warm, regular breaks from sitting"),
       KW(["保持活动", "运动建议", "自我管理", "保暖", "伸展", "坐姿"], ["stay active", "self-management", "exercise advice", "keep warm", "stretches", "sitting breaks"]),
       dose=L("每天短时多次的腰背伸展与步行；每坐30–45分钟起身活动；控制室加穿外套、避免冷气直吹；可局部热敷。说明哪些症状需要立即就医（安全网）。",
              "Short, frequent back stretches and walking every day; get up and move every 30–45 minutes of sitting; wear a jacket in the control room and keep out of the air-con's direct draught; local heat is fine. Tell him which symptoms need urgent care (safety-netting)."),
       risk="none", setFlags=["self-management-advised"],
       indicatedWhen={"decided": "d-disease"},
       response=L("他把伸展动作拍了照片，说回去试试。", "He takes a photo of the stretches and says he'll try them.")),
    iv("refer-imaging", "consult",
       L("转介做腰椎MRI", "Refer for a lumbar spine MRI"),
       KW(["核磁共振", "MRI", "腰椎MRI", "影像检查", "拍片"], ["mri", "lumbar mri", "imaging", "scan", "x-ray"]),
       risk="none",
       response=L("转介信已写好。目前没有红旗征或神经根受累的体征，影像检查不会改变处理，反而可能发现与症状无关的退行性改变、加重担忧。",
                  "The referral is written. With no red flags or signs of nerve-root involvement, imaging would not change management and may show incidental degenerative changes that add to his worry.")),
    iv("refer-ed", "disposition",
       L("立即转介急诊", "Refer to the Emergency Department now"),
       KW(["急诊", "转急诊", "送医院", "紧急转诊"], ["emergency department", "aande", "urgent referral", "send to hospital"]),
       risk="none",
       response=L("目前没有需要急诊处理的表现；转介急诊不会让他得到更合适的照护。若出现马尾综合征征象、进行性无力、发热或外伤等情况，才需要紧急转诊。",
                  "Nothing in his presentation needs emergency care; sending him to the ED would not get him better care. Urgent referral is for signs such as cauda equina symptoms, progressive weakness, fever or significant trauma.")),
    iv("rx-draft", "medication",
       L("提交中药处方第1版", "Submit herbal prescription version 1"),
       KW(["开方", "开中药", "中药处方", "独活寄生汤", "处方第1版"], ["prescribe herbs", "herbal prescription", "du huo ji sheng tang", "prescription version 1", "write the prescription"]),
       dose=L(FORMULA_ZH, FORMULA_EN),
       requires=["records"], scope="medical", risk="low", maxDoses=1, setFlags=["rx-v1-submitted"],
       indicatedWhen={"decided": "d-pattern"},
       response=L("处方第1版已提交药房审核。", "Prescription version 1 has gone to the dispensary for review.")),
    iv("rx-verbal-swap", "medication",
       L("口头同意药房用槲寄生替换桑寄生，处方不改", "Tell the dispensary verbally to swap 槲寄生 for 桑寄生 without changing the prescription"),
       KW(["口头同意替换", "直接换", "照换", "电话同意"], ["verbal swap", "justswapit", "go ahead and substitute", "okbyphone"]),
       risk="moderate", setFlags=["unauthorised-substitution"],
       contraindicatedWhen={"always": True},
       harm=L("发出的药与签署的处方不一致：槲寄生与桑寄生是两味药，替换属于处方变更，必须由处方医师开具新版本处方，否则调剂记录、标签与病历对不上，出了问题也无从追溯。",
              "What is supplied would no longer match the signed prescription: 槲寄生 and 桑寄生 are two different medicinals, so a swap is a change of prescription and needs a new version from the prescriber — otherwise the dispensing record, the label and the notes disagree and nothing can be traced if something goes wrong."),
       response=L("药房记录了这通电话，但仍然按处方第1版标注“待处理”。", "The dispensary notes the call, but version 1 is still marked \"pending\".")),
    iv("rx-v2-substitute", "medication",
       L("开具处方第2版：以槲寄生替换桑寄生（处方医师签名）", "Issue prescription version 2 replacing 桑寄生 with 槲寄生 (signed by the prescriber)"),
       KW(["处方第2版", "改用槲寄生", "新版本处方", "修改处方"], ["prescription version 2", "use visci herba", "new version", "revise the prescription", "amend prescription"]),
       dose=L("第2版：槲寄生15 g（饮片当量）替换桑寄生，其余同第1版；在处方上注明替换理由（桑寄生缺货）；用药记录加入阿司匹林100 mg 每日一次；第1版作废。",
              "Version 2: Visci Herba (槲寄生) 15 g crude-herb equivalent in place of Taxilli Herba (桑寄生), otherwise as version 1; the reason (桑寄生 out of stock) written on the prescription; aspirin 100 mg once daily added to the medication record; version 1 cancelled."),
       requires=["records"], scope="medical", risk="low", checklist=True, maxDoses=1, setFlags=["rx-v2"],
       contraindicatedWhen={"not": {"read": "dispensary-query"}},
       harm=L("还没有看药房的审方意见：没有可回应的问题，新版本无从谈起。", "You have not read the dispensary's query yet: there is nothing to revise against."),
       response=L("第2版已签发，药房确认收到，第1版标记为作废。", "Version 2 is signed; the dispensary acknowledges it and marks version 1 cancelled.")),
    iv("rx-v2-omit", "medication",
       L("开具处方第2版：去掉桑寄生，其余不变（处方医师签名）", "Issue prescription version 2 leaving out 桑寄生, otherwise unchanged (signed by the prescriber)"),
       KW(["去掉桑寄生", "删去桑寄生", "不用桑寄生", "处方第2版"], ["omit taxilli", "leave out", "remove the herb", "prescription version 2"]),
       dose=L("第2版：去掉桑寄生，其余同第1版（杜仲、牛膝仍补肝肾、强筋骨）；复诊时再评估；用药记录加入阿司匹林100 mg 每日一次；第1版作废。",
              "Version 2: Taxilli Herba (桑寄生) left out, otherwise as version 1 (杜仲 and 牛膝 still tonify the liver and kidney and strengthen sinew and bone); reassess at review; aspirin 100 mg once daily added to the medication record; version 1 cancelled."),
       requires=["records"], scope="medical", risk="low", checklist=True, maxDoses=1, setFlags=["rx-v2"],
       contraindicatedWhen={"not": {"read": "dispensary-query"}},
       harm=L("还没有看药房的审方意见：没有可回应的问题，新版本无从谈起。", "You have not read the dispensary's query yet: there is nothing to revise against."),
       response=L("第2版已签发，药房确认收到，第1版标记为作废。", "Version 2 is signed; the dispensary acknowledges it and marks version 1 cancelled.")),
    iv("dispense", "medication",
       L("将现行版本处方交药房调剂并发药", "Release the current prescription version for dispensing and supply"),
       KW(["发药", "调剂", "配药", "取药", "交药房"], ["dispense", "supply", "release to dispensary", "fill the prescription", "collect medicine"]),
       requires=["medications"], risk="low", checklist=True, maxDoses=1, setFlags=["dispensed"],
       contraindicatedWhen={"not": V2},
       harm=L("版本核对未通过：处方第1版仍有未解决的审方意见，药房不会按过期版本发药。先由处方医师开具新版本处方。",
              "Version check failed: prescription version 1 still has an open query, and the dispensary will not supply an outdated version. The prescriber must issue a new version first."),
       response=L("药房按第2版调剂了14包配方颗粒，贴好中英文标签。", "The dispensary fills 14 sachets of granules from version 2 and applies a bilingual label.")),
    iv("counsel-herbs", "other",
       L("中药用法与注意事项交代", "Counsel him on taking the granules and what to watch for"),
       KW(["用药交代", "怎么吃", "服用方法", "注意事项", "用药指导"], ["counsel", "howtotake", "instructions", "medicine advice", "whattowatchfor"]),
       dose=L("每次1包，温水约150 mL冲服，每日2次，饭后；照常服用心脏和血压药，不要自行停阿司匹林；出现皮疹、明显胃部不适、异常瘀青或出血、黑便时停药并联系诊所。",
              "1 sachet in about 150 mL of warm water, twice daily after meals; keep taking his heart and blood-pressure medicines and do not stop the aspirin himself; stop and call the clinic for a rash, marked stomach upset, unusual bruising or bleeding, or black stools."),
       risk="none", setFlags=["counselled"],
       indicatedWhen={"intervened": "dispense", "valid": True},
       response=L("他复述了一遍用法，问能不能晚上那包睡前吃。", "He repeats the instructions back and asks whether the evening sachet can go at bedtime.")),
    iv("gp-letter", "consult",
       L("致函其综合诊所／心脏专科医生：告知中药与针灸方案及阿司匹林的处理", "Write to his polyclinic and heart-clinic doctors: the herbal and acupuncture plan and how aspirin was handled"),
       KW(["写信给医生", "告知家庭医生", "转介信", "通知主诊医生", "沟通信"], ["gp letter", "informhisdoctor", "referral letter", "polyclinic letter", "share the plan"]),
       requires=["records"], scope="medical", risk="none", setFlags=["coordinated"],
       response=L("信件已由患者带回，副本存档。", "The letter goes with him; a copy is filed.")),
    iv("acu-prep", "other",
       L("针刺前准备：手卫生、一次性无菌针、皮肤消毒、锐器盒就位", "Prepare for needling: hand hygiene, single-use sterile needles, skin preparation, sharps bin to hand"),
       KW(["手卫生", "洗手", "消毒", "无菌针", "准备针具", "锐器盒"], ["hand hygiene", "clean needle technique", "sterile needles", "skin prep", "sharps bin", "prepare needles"]),
       risk="none", setFlags=["clean-technique"],
       response=L("治疗车已推到床旁，针具、酒精棉和锐器盒齐备。", "The acupuncture cart is at the couch with needles, swabs and a sharps bin.")),
    iv("acu-position", "positioning",
       L("安排俯卧位并以枕垫支撑（不在坐位下针刺）", "Position him lying prone with pillow support (not seated) for needling"),
       KW(["俯卧", "躺下", "卧位", "上治疗床", "趴着"], ["prone", "lie down", "lying", "onthecouch", "positioning"]),
       posture="lying", destination={"roomKind": "rehabilitation"}, risk="none", setFlags=["positioned-lying"], mitigates=["needle-syncope"],
       response=L("陈先生俯卧在治疗床上，腹下垫枕，面部从床洞露出，说这样很舒服。", "Mr Tan lies prone on the couch with a pillow under his abdomen and his face in the face-hole, and says it's comfortable.")),
    iv("acu-insert", "procedure",
       L("针刺：进针并留针20分钟", "Acupuncture: insert the needles and retain them for 20 minutes"),
       KW(["针刺", "扎针", "进针", "下针", "开始针灸"], ["needle", "insert needles", "start acupuncture", "needling", "acupuncture now"]),
       dose=L("取穴：双侧肾俞（BL23）、大肠俞（BL25）、委中（BL40），右侧环跳（GB30），局部阿是穴3处，共10针；平补平泻，得气后留针20分钟；留针期间观察面色、出汗与主诉。",
              "Points: BL23 (Shenshu), BL25 (Dachangshu) and BL40 (Weizhong) on both sides, GB30 (Huantiao) on the right and 3 local Ashi points — 10 needles; even technique, retained 20 minutes after deqi; watch his colour, sweating and what he says throughout."),
       scope="medical", risk="low", checklist=True, maxDoses=1, setFlags=["needles-in"],
       contraindicatedWhen={"not": {"all": [{"intervened": "explain-consent"}, {"intervened": "acu-prep"}, {"intervened": "acu-position"}]}},
       harm=L("前置条件未满足：进针前需要已记录的知情同意、洁净针刺准备，以及卧位（他有晕针史）。本次进针未执行。",
              "Prerequisites not met: needling needs recorded consent, clean-needle preparation and a lying position (he has fainted with needles before). The needles were not inserted."),
       response=L("10针已进针。他说针下酸胀、腰部发热，没有头晕。", "Ten needles are in. He reports an aching, distending feeling and warmth in the back, and no giddiness.")),
    iv("acu-remove", "procedure",
       L("出针并核对针数（进10支、出10支），弃入锐器盒，检查针孔", "Withdraw the needles, count them against those inserted (10 in, 10 out), discard into the sharps bin and check the sites"),
       KW(["出针", "拔针", "起针", "数针", "核对针数", "清点针"], ["remove needles", "withdraw", "needle count", "count the needles", "take out the needles"]),
       scope="medical", risk="none", checklist=True, maxDoses=1, setFlags=["needles-out"],
       contraindicatedWhen={"not": {"intervened": "acu-insert", "valid": True}},
       harm=L("尚未进针，没有可取出或清点的针。", "No needles have been inserted, so there is nothing to withdraw or count."),
       response=L("出针10支，与进针数一致，全部弃入锐器盒。右委中少量渗血，按压1分钟止。", "Ten needles out, matching the ten in, all into the sharps bin. A small bleed at right BL40 stops with a minute's pressure.")),
    iv("acu-document", "other",
       L("记录本次治疗：穴位、进出针数、留针时间、患者反应与不良事件", "Document the session: points, needles in and out, retention time, his response and any adverse event"),
       KW(["记录治疗", "写治疗记录", "治疗记录", "记录针灸"], ["document the session", "writeitup", "record the treatment", "treatment note"]),
       requires=["records"], scope="medical", risk="none", setFlags=["session-documented"],
       indicatedWhen={"intervened": "acu-remove", "valid": True},
       response=L("治疗记录已保存。", "The session record is saved.")),
    iv("tuina", "procedure",
       L("推拿：腰部椎旁肌放松手法15分钟", "Tuina: 15 minutes of relaxing techniques to the lumbar paraspinal muscles"),
       KW(["推拿", "按摩", "揉法", "滚法"], ["tuina", "massage", "soft tissue", "manual therapy"]),
       dose=L("以滚法、揉法放松腰部椎旁肌，力度以患者可耐受为度，随时询问感受。", "Rolling and kneading techniques to relax the lumbar paraspinal muscles, at a pressure he finds tolerable, checking in with him throughout."),
       scope="medical", risk="low", checklist=True, maxDoses=1,
       contraindicatedWhen={"not": {"intervened": "explain-consent"}},
       harm=L("未取得知情同意：先说明手法、可能的不适并征得同意。", "No consent recorded: explain the technique and possible discomfort and obtain his agreement first."),
       response=L("推拿后他说腰部松了一些。", "After the tuina he says his back feels a little looser.")),
    iv("arrange-followup", "disposition",
       L("预约一周后复诊，明确复诊目标（疼痛、功能、服药情况、不良反应）", "Book a review in one week with stated goals (pain, function, adherence, adverse effects)"),
       KW(["预约复诊", "复诊", "下次来", "一周后复诊", "随访"], ["follow up", "follow-up", "review in a week", "book a review", "next appointment"]),
       risk="none", setFlags=["followup-booked"],
       indicatedWhen={"intervened": "dispense", "valid": True},
       response=L("前台预约了下周同一时间，并请他带回剩余药包和服药记录。", "Reception books the same time next week and asks him to bring back any sachets left and his dose diary.")),
    # --- review ---------------------------------------------------------------------------------
    iv("adherence-plan", "other",
       L("按其班次调整服药与自我管理计划", "Fit the dosing and self-management plan to his shifts"),
       KW(["调整服药", "依从性", "提醒", "服药时间", "配合班次"], ["adherence plan", "reminders", "dosing times", "fit his shifts", "make it easier"]),
       dose=L("第二包改在“起床后第二顿饭后”服用（夜班日同样适用），手机设提醒；剩余药包继续用完；恢复每天两次伸展，控制室每45分钟起身，穿外套；下次带服药记录。",
              "Move the second sachet to \"after the second meal after waking\" (which also works on night shifts) with a phone reminder; finish the remaining sachets; restart the stretches twice a day, get up every 45 minutes in the control room and wear a jacket; bring the dose diary next time."),
       risk="none", setFlags=["adherence-planned"],
       indicatedWhen={"decided": "d-followup"},
       response=L("他把提醒设在手机上：“这样夜班也记得住。”", "He sets the reminder on his phone: \"That I can remember, even on nights.\"")),
    iv("continue-course", "disposition",
       L("维持现行处方版本，继续既定针灸疗程（每周两次，再两周），两周后复诊", "Keep the current prescription version, continue the planned acupuncture course (twice weekly for two more weeks) and review in two weeks"),
       KW(["继续治疗", "继续疗程", "继续针灸", "维持方案", "两周后复诊"], ["continue treatment", "continue the course", "keep going", "carry on", "review in two weeks"]),
       risk="none", setFlags=["course-continued"],
       indicatedWhen={"decided": "d-followup"},
       response=L("下两周的针灸已排好，药房按第2版续配。", "The next two weeks of acupuncture are booked, and the dispensary repeats version 2.")),
    iv("switch-damp-heat", "medication",
       L("改用清热利湿方（四妙丸类）", "Switch to a heat-clearing, damp-draining formula (四妙丸 type)"),
       KW(["四妙丸", "清热利湿", "改方", "湿热方"], ["si miao", "clear heat", "damp-heat formula", "switch formula"]),
       scope="medical", risk="low",
       contraindicatedWhen={"always": True},
       harm=L("与证不符：他畏寒、喜热饮、遇冷加重、舌淡苔白、脉沉细，是寒湿而非湿热。苦寒清热之品会伤阳，可能加重寒湿。部分改善的原因是依从性和诱因，不是辨证错误。",
              "It does not fit the pattern: he feels the cold, likes hot drinks, is worse in cold and damp, has a pale tongue with a white coating and a deep, thready pulse — cold-damp, not damp-heat. Bitter-cold heat-clearing herbs injure yang and may make cold-damp worse. The partial response comes from adherence and exposure, not a wrong pattern."),
       response=L("新处方已开出。", "The new prescription is written.")),
    iv("double-dose", "medication",
       L("将颗粒剂量加倍，以弥补漏服", "Double the granule dose to make up for missed doses"),
       KW(["加倍", "加量", "补服", "双倍"], ["double the dose", "increase dose", "make up doses", "twiceasmuch"]),
       scope="medical", risk="moderate",
       contraindicatedWhen={"always": True},
       harm=L("漏服不需要也不应该补加倍：剂量超过处方，胃肠不适与相互作用的风险增加，也解决不了漏服的原因。应调整服药时间、设提醒。",
              "Missed doses are not made up by doubling: it exceeds the prescribed dose, adds to the risk of stomach upset and interactions, and does nothing about why doses were missed. Change the timing and add reminders instead."),
       response=L("剂量已改。", "The dose is changed.")),
    iv("stop-aspirin", "medication",
       L("建议患者服中药期间停用阿司匹林", "Advise him to stop aspirin while he takes the herbs"),
       KW(["停阿司匹林", "停用阿司匹林", "暂停阿司匹林", "停掉血稀药"], ["stop aspirin", "hold the aspirin", "stop the blood thinner", "pause aspirin"]),
       scope="medical", risk="high",
       contraindicatedWhen={"always": True},
       harm=L("冠脉支架术后的长期抗血小板治疗不能由中医诊所停用：停药会增加支架血栓和心肌梗死风险。相互作用的处理是调整中药、观察与告知其心脏科医生，而不是停阿司匹林。",
              "Long-term antiplatelet therapy after a coronary stent is not for a TCM clinic to stop: stopping it raises the risk of stent thrombosis and heart attack. The interaction is managed by adjusting the herbs, monitoring and telling his cardiologist — not by stopping aspirin."),
       response=L("陈先生迟疑地说：“心脏科医生说过这粒不能停……”", "Mr Tan hesitates: \"The heart doctor said never to stop that one…\"")),
]


# ---------------------------------------------------------------------------------------------
# Learning design: phases, objectives, decisions, rubric, safety gates
# ---------------------------------------------------------------------------------------------

PHASES = [
    {"id": "consult", "label": L("初诊：问诊与四诊", "First visit: history and the four examinations"),
     "description": L("社区中医诊所的初诊：问诊、四诊合参与安全筛查。", "First visit at the community TCM clinic: history, the four examinations and the safety screen."),
     "learnerSwitchable": True},
    {"id": "treatment", "label": L("初诊：处方、审方与针灸", "First visit: prescription, review and acupuncture"),
     "description": L("开方并处理药房的审方意见，完成首次针灸。", "Prescribe, resolve the dispensary's query and give the first acupuncture session."),
     "learnerSwitchable": False,
     "enterWhen": {"all": [{"decided": "d-disease"}, {"decided": "d-pattern"}]}},
    {"id": "followup", "label": L("一周后复诊", "Review one week later"),
     "description": L("一周后回到诊室：疗效、执行情况与不良反应。", "Back in the consulting room a week later: response, what was actually done, and adverse effects."),
     "learnerSwitchable": False,
     "enterWhen": {"all": [{"intervened": "dispense", "valid": True}, {"intervened": "acu-remove", "valid": True}, {"intervened": "arrange-followup"}]},
     "location": {"roomKind": "consult"}},
]

OBJECTIVES = [
    {"id": "o-inquiry", "title": L("问诊并筛查危险信号", "Take the history and screen for danger signs"),
     "short": L("问诊", "History"),
     "hint": L("先听他讲这次的经过，再系统问：部位与放射、加重缓解、下肢神经与大小便、全身症状，以及既往史、用药与过敏。",
               "Let him tell the story, then ask systematically: site and spread, what worsens and eases it, leg nerves and bladder or bowel, systemic symptoms, then past history, medicines and allergies."),
     "guidance": L("在诊室与陈先生面谈。", "Talk with Mr Tan in the consulting room."),
     "completeWhen": {"all": [{"asked": h} for h in ["h-presenting", "h-site", "h-modifiers", "h-redflag-neuro", "h-redflag-ce", "h-redflag-systemic", "h-pmh", "h-meds", "h-allergies"]]},
     "waypoints": [{"target": "patient"}]},
    {"id": "o-four-exam", "title": L("完成四诊与体格检查", "Complete the four examinations and the physical screen"),
     "short": L("四诊", "Four examinations"),
     "hint": L("望（神色形态、舌）、闻（声音、气味）、切（脉、腰部），再加下肢神经系统与直腿抬高检查。",
               "Inspection (spirit, complexion, build, tongue), listening and smelling (voice, odour), palpation (pulse, lower back), plus the lower-limb neurological check and straight-leg raise."),
     "guidance": L("在诊室内为他检查。", "Examine him in the consulting room."),
     "completeWhen": {"all": [{"examined": e} for e in ["e-general", "e-voice-odour", "e-tongue", "e-pulse", "e-lumbar-palp", "e-slr", "e-neuro"]]},
     "waypoints": [{"target": "patient"}]},
    {"id": "o-assess", "title": L("权衡证据，作出诊断与辨证", "Weigh the evidence and make the diagnosis and pattern assessment"),
     "short": L("评估", "Assessment"),
     "hint": L("先看候诊区的自助机舌象照片，想一想它的拍摄条件是否可信；再结合全部四诊判断疾病与证候。",
               "Look at the kiosk tongue photo from the waiting area and ask how far its capture conditions can be trusted; then judge the disease and the pattern from all four examinations."),
     "guidance": L("在病历终端调阅记录，在病例板上作答。", "Open the records at a terminal and answer on the case board."),
     "completeWhen": {"all": [{"decided": "d-evidence"}, {"decided": "d-disease"}, {"decided": "d-pattern"}]},
     "waypoints": [{"unless": {"read": "intake-tongue-photo"}, "target": "records"}, {"target": "board"}]},
    {"id": "o-prescribe", "title": L("开方、处理审方意见并发药", "Prescribe, resolve the dispensary's query and supply the medicine"),
     "short": L("处方", "Prescription"),
     "hint": L("提交处方后到病历终端查看药房的审方意见；处方的任何改变都要留下可追溯的记录，再交药房调剂并做用药交代。",
               "After submitting the prescription, read the dispensary's response at a records terminal; any change to a prescription must leave a traceable record before it is filled and explained to him."),
     "guidance": L("处方在病历终端提交；发药在中药房。", "Prescriptions are submitted at a records terminal; supply happens at the herbal dispensary."),
     "completeWhen": {"all": [{"decided": "d-rx-review"}, {"intervened": "dispense", "valid": True}, {"intervened": "counsel-herbs"}]},
     "waypoints": [{"unless": {"intervened": "rx-draft"}, "target": "records"}, {"unless": {"read": "dispensary-query"}, "target": "records"}, {"target": "medications"}]},
    {"id": "o-acupuncture", "title": L("安全完成首次针灸并安排复诊", "Give the first acupuncture session safely and book the review"),
     "short": L("针灸", "Acupuncture"),
     "hint": L("进针前确认同意、准备与体位都已到位；出针时与进针数核对；记录本次治疗，再预约复诊。",
               "Before needling, make sure consent, preparation and position are in place; on withdrawal, check the count against what went in; document the session, then book the review."),
     "guidance": L("在针灸推拿治疗室。", "In the acupuncture and tuina treatment room."),
     "completeWhen": {"all": [{"intervened": "acu-remove", "valid": True}, {"intervened": "acu-document"}, {"intervened": "arrange-followup"}]},
     "waypoints": [{"target": "patient"}]},
    {"id": "o-followup", "title": L("一周复诊：核对执行情况并修订方案", "One-week review: check what was actually done and revise the plan"),
     "short": L("复诊", "Review"),
     "hint": L("先弄清楚他实际接受了哪些治疗、实际服了多少药、有没有不良反应，再判断疗效有限的原因。",
               "First establish what treatment he actually received, how much medicine he actually took and whether there were adverse effects; then judge why the response was limited."),
     "guidance": L("在诊室与陈先生复诊。", "Review Mr Tan in the consulting room."),
     "completeWhen": {"all": [{"decided": "d-followup"}, {"intervened": "adherence-plan"}, {"intervened": "continue-course"}]},
     "waypoints": [{"target": "patient"}]},
]


def opt(id, correct, text, feedback):
    return {"id": id, "text": text, "correct": correct, "feedback": feedback}


DECISIONS = [
    {
        "id": "d-evidence", "kind": "single",
        "prompt": L("自助机舌象照片显示似乎是黄褐色厚苔。在用它辨证之前，你怎么处理这条证据？",
                    "The kiosk photo shows what looks like a thick yellow-brown coating. Before you use it for pattern differentiation, how do you handle this piece of evidence?"),
        "requires": {"read": "intake-tongue-photo", "phase": "consult"},
        "need": L("先调阅候诊区自助机拍摄的舌象照片。", "First open the tongue photo the kiosk took in the waiting area."),
        "options": [
            opt("recheck", True,
                L("视为不可靠证据（暖光、无色卡、可能染苔）：询问来诊前饮食，漱口后在自然光或标准光源下重新望舌或采集，再用于辨证",
                  "Treat it as unreliable (warm light, no colour card, possible staining): ask what he ate or drank, then re-inspect or recapture the tongue after rinsing, in daylight or under standard light, before using it"),
                L("正确。暖色光会让舌色偏红、苔色偏黄；画面中没有色卡就无法校色；咖啡、茶、咖椰等饮食可染苔。证据有来源、时间和质量，先补足可靠证据再辨证。",
                  "Correct. Warm light makes the tongue look redder and the coating yellower; without a colour card in frame the colour cannot be checked; coffee, tea and kaya can stain the coating. Evidence has a source, a time and a quality — obtain reliable evidence before you reason on it.")),
            opt("trust-machine", False,
                L("机器拍的比肉眼客观，直接按黄厚苔向湿热方向辨证",
                  "A machine photo is more objective than the eye — take the thick yellow coating at face value and work towards damp-heat"),
                L("不对。照片只是在特定条件下的一次采集，机器本身已提示颜色校验未通过。以染苔辨为湿热，是典型的证据质量错误。",
                  "No. A photo is one capture under particular conditions, and the kiosk itself flagged the colour check as failed. Calling damp-heat from a stained coating is a classic evidence-quality error.")),
            opt("drop-tongue", False,
                L("既然照片不可靠，就完全放弃舌诊，只凭脉象和问诊辨证",
                  "Since the photo is unreliable, drop tongue diagnosis altogether and rely on the pulse and the history"),
                L("不对。问题出在这次采集，而不是舌诊本身。重新望舌很容易，丢掉一整个诊察维度会削弱辨证。",
                  "No. The problem is this capture, not tongue diagnosis itself. Re-inspecting is easy; discarding a whole channel of the four examinations weakens the assessment.")),
            opt("scrape", False,
                L("请他把舌苔刮掉后再拍一张", "Ask him to scrape his tongue clean and photograph it again"),
                L("不对。刮舌会去掉舌苔本身，破坏要观察的对象。漱口即可去除饮食染色。",
                  "No. Scraping removes the coating itself — the very thing you want to see. A rinse is enough to clear food staining.")),
        ],
    },
    {
        "id": "d-disease", "kind": "single",
        "prompt": L("结合病史与体格检查，西医层面应如何判断？现在需要影像检查或转诊吗？",
                    "From the history and examination, what is the biomedical assessment, and does he need imaging or referral now?"),
        "requires": {"all": [{"asked": "h-redflag-neuro"}, {"asked": "h-redflag-ce"}, {"asked": "h-redflag-systemic"}, {"examined": "e-neuro"}, {"examined": "e-slr"}]},
        "need": L("先完成危险信号问诊、下肢神经系统检查与直腿抬高试验。", "First complete the danger-sign questions, the lower-limb neurological examination and the straight-leg raise."),
        "options": [
            opt("nslbp", True,
                L("复发性非特异性（机械性）腰痛，伴非根性的臀部牵涉痛；无红旗征、无神经根受累——目前不需要影像或转诊，并给予安全网建议",
                  "Recurrent non-specific (mechanical) low back pain with non-radicular referral to the buttock; no red flags and no nerve-root involvement — no imaging or referral now, with clear safety-netting"),
                L("正确。疼痛不过膝、无麻木无力、直腿抬高阴性、神经系统检查正常，也没有大小便、全身或外伤方面的红旗征。NICE NG59：非特异性腰痛在非专科场所不常规做影像检查。",
                  "Correct. The pain stops above the knee, there is no numbness or weakness, the straight-leg raise is negative and the neurological examination normal, with no bladder, bowel, systemic or trauma red flags. NICE NG59: do not routinely offer imaging for non-specific low back pain in a non-specialist setting.")),
            opt("disc", False,
                L("腰椎间盘突出伴坐骨神经痛，应尽快安排腰椎MRI", "Lumbar disc herniation with sciatica — arrange a lumbar MRI soon"),
                L("不对。坐骨神经痛表现为放射至膝以下的腿痛，常伴神经根体征；他的疼痛不过膝、直腿抬高阴性、神经系统检查正常。MRI不会改变处理。",
                  "No. Sciatica is leg pain radiating below the knee, often with nerve-root signs; his pain stays above the knee, the straight-leg raise is negative and the neurological examination is normal. An MRI would not change management.")),
            opt("degenerative", False,
                L("腰椎退行性病变所致，应拍腰椎X线确认", "Degenerative spine disease is the cause — order a lumbar X-ray to confirm it"),
                L("不对。退行性改变在这个年龄很常见，与症状关联很弱；X线不会改变非特异性腰痛的处理，还会带来不必要的辐射和担忧。",
                  "No. Degenerative changes are very common at his age and correlate poorly with symptoms; an X-ray would not change the management of non-specific low back pain and adds radiation and worry.")),
            opt("cauda", False,
                L("可能是马尾综合征，需要立即送急诊", "Possible cauda equina syndrome — send him to the Emergency Department now"),
                L("不对。他没有大小便功能障碍、鞍区麻木或下肢神经缺损。这些征象一旦出现才需要紧急转诊——这正是安全网建议要告诉他的内容。",
                  "No. He has no bladder or bowel disturbance, no saddle numbness and no neurological deficit. Emergency referral is for when those appear — which is exactly what the safety-netting advice tells him.")),
        ],
    },
    {
        "id": "d-pattern", "kind": "single",
        "prompt": L("综合四诊，本次腰痛最能被证据支持的证候是？", "Bringing the four examinations together, which pattern is best supported by the evidence?"),
        "requires": {"all": [{"decided": "d-evidence"}, {"any": [{"examined": "e-tongue"}, {"read": "tongue-recapture"}]}, {"examined": "e-pulse"}, {"asked": "h-modifiers"}, {"asked": "h-coldheat"}]},
        "need": L("先处理舌象证据的质量问题，并完成望舌、切脉以及寒热、加重缓解因素的问诊。",
                  "First deal with the quality of the tongue evidence, and complete the tongue and pulse examinations and the questions on cold and heat and on what worsens and eases the pain."),
        "options": [
            opt("cold-damp", True,
                L("寒湿痹阻，兼肝肾不足", "Cold-damp obstruction with underlying liver–kidney insufficiency"),
                L("正确。腰部冷重酸痛、遇寒湿加重、得温则减、畏寒喜热饮、腰部皮温偏凉，属寒湿痹阻；反复三年、腰膝酸软、尺脉弱、舌淡胖有齿痕，提示肝肾不足（兼脾虚湿盛）。支持证据与反对证据都应写入评估。",
                  "Correct. A cold, heavy ache worse in cold and damp and better with warmth, cold intolerance with a liking for hot drinks, and a cool lower back point to cold-damp obstruction; three years of recurrence, sore weak knees, weak chi pulses and a pale, swollen, tooth-marked tongue point to underlying liver–kidney insufficiency (with spleen deficiency and damp). Record the evidence for and against.")),
            opt("damp-heat", False,
                L("湿热蕴结", "Damp-heat accumulation"),
                L("不对。湿热腰痛多见热痛、遇热加重、口苦、小便黄赤、苔黄腻、脉滑数。唯一的“黄苔”来自染色和暖光下的照片，重新采集后为白腻苔。",
                  "No. Damp-heat lumbago brings hot pain worse with heat, a bitter taste, dark urine, a yellow greasy coating and a slippery, rapid pulse. The only \"yellow coating\" came from a stained photo under warm light; recaptured, it is white and greasy.")),
            opt("stasis", False,
                L("瘀血阻络", "Blood stasis obstructing the collaterals"),
                L("不对。瘀血腰痛多为刺痛、痛处固定拒按、夜间加重，舌紫暗或有瘀斑、舌下络脉迂曲。他的疼痛是沉重酸痛，舌下络脉不迂曲。急性扭伤可兼瘀，但不是主证。",
                  "No. Blood-stasis lumbago is stabbing, fixed and worse when pressed and at night, with a purple tongue or spots and distended sublingual veins. His pain is a heavy ache and his sublingual veins are normal. A strain can add some stasis, but it is not the main pattern.")),
            opt("kidney-yang", False,
                L("单纯肾阳虚衰，无外邪", "Kidney-yang decline alone, with no external pathogen"),
                L("不完全对。本虚确实存在，但遇冷湿明显加重、腰部冷重、苔白腻，说明寒湿之邪仍在。只补不祛，标证难除。",
                  "Not quite. The underlying deficiency is real, but clear worsening in cold and damp, a cold heavy back and a white greasy coating show that cold-damp is still present. Tonifying alone, without dispelling it, leaves the presenting problem untreated.")),
        ],
    },
    {
        "id": "d-rx-review", "kind": "multiple",
        "prompt": L("药房暂缓了处方第1版，并提出两点意见。你接下来怎么做？（选出所有正确做法）",
                    "The dispensary has put prescription version 1 on hold with two queries. What do you do next? (Select all that apply.)"),
        "requires": {"all": [{"read": "dispensary-query", "phase": "treatment"}, {"any": [{"asked": "h-antithrombotic"}, {"read": "prior-records"}]}]},
        "need": L("先调阅药房的审方意见，并补全他的用药史。", "First read the dispensary's query and complete his medication history."),
        "options": [
            opt("new-version", True,
                L("不由药房自行替换：由处方医师开具签名的新版本处方（写明换用槲寄生，或去掉桑寄生），第1版作废",
                  "Do not let the dispensary swap on its own: the prescriber issues a new signed prescription version (naming 槲寄生 as the replacement, or leaving 桑寄生 out) and version 1 is cancelled"),
                L("正确。两种改法都可以接受，关键是改动由处方医师决定、形成新版本并留下记录，药房只按现行版本调剂。",
                  "Correct. Either change is acceptable; what matters is that the prescriber decides, a new version records it, and the dispensary fills only the current version.")),
            opt("aspirin-managed", True,
                L("把阿司匹林100 mg补入用药记录；当归、川芎保持常规剂量或去掉，告诉他留意瘀青、出血与黑便，并告知他的主诊医生",
                  "Add aspirin 100 mg to his medication record; keep 当归 and 川芎 at usual doses or leave them out, tell him to watch for bruising, bleeding and black stools, and let his own doctor know"),
                L("正确。活血药与阿司匹林合用增加出血风险的证据多为理论推断或个案，但足以要求记录、观察与告知。两种用药调整都可辩护。",
                  "Correct. Evidence that blood-activating herbs add to aspirin's bleeding risk is mostly theoretical or from case reports, but it is enough to require recording, monitoring and telling his doctor. Either dosing choice is defensible.")),
            opt("phone-ok", False,
                L("电话里同意替换，处方保持第1版不改，事后再补记录", "Agree the swap by phone, leave version 1 as the record and annotate it later"),
                L("不对。这样发出的药与签署的处方不一致，调剂记录、标签和病历都对不上，正是版本控制要防止的执行差错。",
                  "No. What is supplied would then differ from the signed prescription, and the dispensing record, label and notes would disagree — exactly the execution error version control exists to prevent.")),
            opt("stop-aspirin", False,
                L("建议他服中药期间先停阿司匹林", "Advise him to stop aspirin while he takes the herbs"),
                L("不对。他放过冠脉支架，长期抗血小板治疗不能由中医诊所停用，停药会增加支架血栓风险。调整的是中药，不是阿司匹林。",
                  "No. He has a coronary stent; long-term antiplatelet therapy is not a TCM clinic's to stop, and stopping it raises the risk of stent thrombosis. Adjust the herbs, not the aspirin.")),
            opt("same-herb", False,
                L("桑寄生和槲寄生名字相近，可视为同一味药直接互换", "桑寄生 and 槲寄生 have similar names, so treat them as the same herb and swap freely"),
                L("不对。两者来源不同（桑寄生为桑寄生科钝果寄生属植物，槲寄生为槲寄生属植物），药典分列；功效相近不等于同一药材。名称相近正是调剂差错的高风险点。",
                  "No. They come from different plants (Taxillus versus Viscum) and have separate Pharmacopoeia monographs; similar actions do not make them the same medicinal. Look-alike names are precisely where dispensing errors happen.")),
        ],
    },
    {
        "id": "d-followup", "kind": "single",
        "prompt": L("一周复诊：疼痛从6分降到4分，但改善没有维持。最能解释这一结果的是什么？下一步怎么做？",
                    "At one week his pain is down from 6 to 4 out of 10, but the gain has not held. What best explains this, and what next?"),
        "requires": {"all": [{"asked": "h-fu-status"}, {"asked": "h-fu-adherence"}, {"asked": "h-fu-adverse"}, {"asked": "h-fu-redflags"}, {"read": "sachet-count", "phase": "followup"}, {"examined": "e-fu-neuro"}]},
        "need": L("先问清楚这一周的情况、服药情况、不良反应与危险信号，清点剩余药包，并复查下肢神经系统。",
                  "First ask about the week, how he took the medicine, adverse effects and danger signs, count the remaining sachets and repeat the lower-limb neurological check."),
        "options": [
            opt("adherence", True,
                L("部分有效，主要受服药依从性（晚上漏服）和持续诱因（久坐、冷气、停了运动）限制；无危险信号，证候判断仍成立——维持评估，按班次调整服药与自我管理，继续既定针灸疗程并再评估",
                  "A partial response limited mainly by adherence (missed evening doses) and continuing exposure (long sitting in cold air-con, exercises stopped); no danger signs and the pattern still holds — keep the assessment, fit dosing and self-management to his shifts, continue the planned acupuncture course and review again"),
                L("正确。执行记录显示他只服了约一半的药，诱因也没有改变；症状、舌脉与初诊一致，没有新的危险信号。原评估仍可辩护，需要修订的是执行方案。",
                  "Correct. The execution record shows he took about half the medicine and the exposure has not changed; his symptoms, tongue and pulse match the first visit and there are no new danger signs. The original assessment still stands; it is how the plan is carried out that needs revising.")),
            opt("wrong-pattern", False,
                L("证候判断错误，应改辨为湿热，换用清热利湿方", "The pattern was wrong — re-label it as damp-heat and switch to a heat-clearing, damp-draining formula"),
                L("不对。没有任何新的湿热证据：舌淡苔白、脉沉细、仍畏寒。只吃了一半的药，不能据此判断方证不符。",
                  "No. There is no new evidence of damp-heat: the tongue is pale with a white coating, the pulse deep and thready, and he still feels the cold. Having taken half the medicine, he cannot show that the formula failed to fit the pattern.")),
            opt("mri", False,
                L("一周还没好，应安排腰椎MRI", "He is not better after a week — arrange a lumbar MRI"),
                L("不对。症状在改善，神经系统检查正常，也没有新的危险信号。一周内未痊愈不是影像检查的指征。",
                  "No. He is improving, the neurological examination is normal and there are no new danger signs. Not being cured within a week is not an indication for imaging.")),
            opt("double", False,
                L("把颗粒剂量加倍以弥补漏服", "Double the granule dose to make up for the missed doses"),
                L("不对。加倍超过处方剂量，增加不良反应和相互作用风险，也没有解决漏服的原因。",
                  "No. Doubling exceeds the prescribed dose, adds to the risk of adverse effects and interactions, and does nothing about why doses were missed.")),
            opt("stop-acu", False,
                L("针刺处出现瘀青，说明服阿司匹林者不宜针灸，应停止针灸", "The bruise at a needle site shows acupuncture is unsafe on aspirin — stop it"),
                L("不对。小而无痛的瘀斑是常见轻微不良反应，应记录并在出针时延长按压；服阿司匹林不是针刺的绝对禁忌。",
                  "No. A small, painless bruise is a common minor adverse effect — document it and press a little longer on withdrawal; aspirin is not an absolute contraindication to acupuncture.")),
        ],
    },
]

RUBRIC = [
    {"id": "r-redflags", "domain": "history", "weight": 3, "critical": True,
     "text": L("系统筛查腰痛危险信号（神经、大小便与鞍区、全身症状）并完成下肢神经系统检查",
               "Screened for danger signs (neurological, bladder, bowel and saddle, systemic) and examined the lower-limb nerves"),
     "met": {"all": [{"asked": "h-redflag-neuro"}, {"asked": "h-redflag-ce"}, {"asked": "h-redflag-systemic"}, {"examined": "e-neuro"}]}},
    {"id": "r-inquiry", "domain": "history", "weight": 2,
     "text": L("问诊覆盖部位与放射、加重缓解、寒热、腰膝症状、既往史与用药",
               "Inquiry covered site and spread, aggravating and easing factors, cold and heat, back and knee symptoms, past history and medicines"),
     "met": {"all": [{"asked": h} for h in ["h-site", "h-modifiers", "h-coldheat", "h-knees-fatigue", "h-pmh", "h-meds"]]}},
    {"id": "r-antithrombotic", "domain": "safety", "weight": 2,
     "text": L("发现并核实他在服阿司匹林（追问或调阅自带用药清单）", "Found and confirmed his aspirin (by asking specifically or reading the medication list he brought)"),
     "met": {"any": [{"asked": "h-antithrombotic"}, {"read": "prior-records"}]}},
    {"id": "r-four-exam", "domain": "examination", "weight": 2,
     "text": L("完成望、闻、切诊（神色形态、舌、声音气味、脉、腰部触诊）", "Completed inspection, listening and smelling, and palpation (spirit and build, tongue, voice and odour, pulse, lumbar palpation)"),
     "met": {"all": [{"examined": e} for e in ["e-general", "e-tongue", "e-voice-odour", "e-pulse", "e-lumbar-palp"]]}},
    {"id": "r-evidence", "domain": "investigations", "weight": 2,
     "text": L("识别自助机舌象照片的质量问题并取得可靠舌象", "Recognised the kiosk tongue photo's quality problem and obtained a reliable view of the tongue"),
     "met": {"all": [{"decidedFirstTry": "d-evidence"}, {"any": [{"examined": "e-tongue"}, {"read": "tongue-recapture"}]}]}},
    {"id": "r-disease", "domain": "diagnosis", "weight": 2,
     "text": L("首次即正确判断为无红旗征的非特异性腰痛，不需影像", "Judged non-specific low back pain without red flags and no need for imaging, first time"),
     "met": {"decidedFirstTry": "d-disease"}},
    {"id": "r-pattern", "domain": "diagnosis", "weight": 3,
     "text": L("首次即作出有证据支持的证候判断", "Reached the evidence-supported pattern assessment first time"),
     "met": {"decidedFirstTry": "d-pattern"}},
    {"id": "r-rx-review", "domain": "management", "weight": 2,
     "text": L("首次即正确处理药房的两点审方意见", "Handled both dispensary queries correctly first time"),
     "met": {"decidedFirstTry": "d-rx-review"}},
    {"id": "r-rx-version", "domain": "safety", "weight": 3, "critical": True,
     "text": L("只有在处方医师签发新版本后才发药（版本核对通过）", "Medicine supplied only after the prescriber issued a new version (the version check passed)"),
     "met": {"all": [{"intervened": "dispense", "valid": True}, {"not": {"intervened": "rx-verbal-swap"}}]}},
    {"id": "r-acu-sequence", "domain": "safety", "weight": 3,
     "text": L("按顺序完成针灸流程：同意 → 准备 → 卧位 → 进针 → 出针核对", "Followed the acupuncture sequence: consent → preparation → lying position → needling → withdrawal and count"),
     "met": {"inOrder": ["explain-consent", "acu-prep", "acu-position", "acu-insert", "acu-remove"]}},
    {"id": "r-needle-count", "domain": "safety", "weight": 3, "critical": True,
     "text": L("出针时核对针数，没有针遗留", "Counted the needles out against those in, leaving none behind"),
     "met": {"intervened": "acu-remove", "valid": True},
     "scoredWhen": {"intervened": "acu-insert", "valid": True}},
    {"id": "r-self-management", "domain": "management", "weight": 1,
     "text": L("给予保持活动、运动与工作姿势方面的自我管理建议", "Gave self-management advice on staying active, exercise and posture at work"),
     "met": {"intervened": "self-management"}},
    {"id": "r-no-imaging", "domain": "efficiency", "weight": 1,
     "text": L("没有做不必要的影像转介", "Avoided an unnecessary imaging referral"),
     "met": {"not": {"intervened": "refer-imaging"}},
     "scoredWhen": {"any": [{"attempted": "d-disease"}, {"intervened": "refer-imaging"}]}},
    {"id": "r-coordination", "domain": "management", "weight": 1,
     "text": L("把中药、针灸与阿司匹林的处理告知他的主诊医生", "Told his own doctors about the herbs, the acupuncture and how aspirin was handled"),
     "met": {"intervened": "gp-letter"}},
    {"id": "r-followup", "domain": "management", "weight": 3,
     "text": L("复诊时依据执行记录找出疗效有限的原因，并相应修订方案", "At review, used the execution record to find why the response was limited and revised the plan to match"),
     "met": {"all": [{"decidedFirstTry": "d-followup"}, {"intervened": "adherence-plan"}, {"not": {"intervened": "switch-damp-heat"}}, {"not": {"intervened": "double-dose"}}]},
     "scoredWhen": {"any": [{"phase": "followup"}, {"intervened": "switch-damp-heat"}, {"intervened": "double-dose"}]}},
    {"id": "r-comm-consent", "domain": "communication", "weight": 2,
     "text": L("用他偏好的语言解释病情与方案，回应他的担忧并取得知情同意", "Explained the condition and plan in his preferred language, answered his concerns and obtained informed consent"),
     "judgeGuidance": L("学员是否用通俗的华语（或他选择的语言）说明这是常见的非特异性腰痛、不需要开刀；回应他对椎间盘突出和中西药冲突的担忧；说明针灸与中药的获益、风险和其他选择；因既往晕针安排卧位；并确认他理解后再取得同意？",
                        "Did the learner explain in plain Mandarin (or his chosen language) that this is common non-specific back pain that does not need surgery; address his fears about a slipped disc and herb–medicine clashes; set out the benefits, risks and alternatives of acupuncture and herbs; plan a lying position because of his previous faint; and check understanding before taking consent?")},
    {"id": "r-comm-review", "domain": "communication", "weight": 1,
     "text": L("复诊时不带评判地了解漏服原因，与他共同制定可行方案", "At review, explored missed doses without judgement and agreed a workable plan with him"),
     "judgeGuidance": L("学员是否以开放、不责备的方式询问漏服和停做运动的原因（夜班、忘记、口味），并与他一起找到适合班次的办法，而不是简单重复医嘱？",
                        "Did the learner ask openly and without blame why doses and exercises were missed (night shifts, forgetting, the taste), and work out with him a plan that fits his shifts, rather than simply repeating the instructions?")},
]

SAFETY_GATES = [
    {"id": "g-unauthorised-substitution", "verdict": "safety-critical", "capPercent": 40,
     "label": L("未经新版本处方即口头同意替换药材", "A herb substitution agreed verbally without a new prescription version"),
     "when": {"intervened": "rx-verbal-swap"}},
    {"id": "g-needles-unaccounted", "verdict": "safety-critical", "capPercent": 40,
     "label": L("已进针但未出针核对针数", "Needles inserted but never withdrawn and counted"),
     "when": {"all": [{"intervened": "acu-insert", "valid": True}, {"not": {"intervened": "acu-remove", "valid": True}}]}},
    {"id": "g-stop-antiplatelet", "verdict": "safety-critical", "capPercent": 40,
     "label": L("建议冠脉支架术后患者停用阿司匹林", "Advised a patient with a coronary stent to stop aspirin"),
     "when": {"intervened": "stop-aspirin"}},
    {"id": "g-outdated-version-intercepted", "verdict": "complication",
     "label": L("试图按未解决审方意见的处方版本发药（已被版本核对拦截）", "Supply attempted from a prescription version with an open query (intercepted by the version check)"),
     "when": {"intervened": "dispense", "valid": False}},
    {"id": "g-needling-refused", "verdict": "complication",
     "label": L("在前置条件未满足时尝试进针（已被拦截）", "Needling attempted before its prerequisites were met (intercepted)"),
     "when": {"intervened": "acu-insert", "valid": False}},
]

NPCS = [
    {"role": "nurse", "name": L("Siti（诊所助理）", "Siti (clinic assistant)"),
     "knowledge": L("负责挂号后的接待、自助问诊机的使用指导、治疗室准备（床单、枕垫、治疗车、锐器盒）和针数登记表。知道自助机舌象照片需要色卡和标准光，候诊时刚吃喝过的患者照片常不可靠——只讲操作规范，不解读具体照片。可帮忙推治疗车、协助患者俯卧、联系药房和前台预约复诊。不作诊断、不开方、不进针或出针。",
                        "Handles reception after registration, helps patients use the intake kiosk, prepares the treatment room (couch roll, pillows, acupuncture cart, sharps bin) and keeps the needle-count sheet. Knows kiosk tongue photos need the colour card and standard light, and that photos of patients who have just eaten or drunk are often unreliable — she explains the procedure, never reads a particular photo. Can bring the cart, help a patient lie prone, call the dispensary and book the review with reception. Does not diagnose, prescribe, insert or withdraw needles."),
     "interprets": []},
    {"role": "pharmacist", "name": L("林先生（中药调剂）", "Mr Lim (TCM dispensing)"),
     "knowledge": L("负责审方与调剂。原则：药房只按处方医师签署的现行版本调剂，任何替换或改动都要新版本处方；不接受口头改方。可解释：桑寄生与槲寄生来源不同、药典分列、功效相近但不是同一药材；配方颗粒按饮片当量开具；活血药（当归、川芎）与抗血小板药合用的出血风险证据多为理论推断或个案，处理方式是记录、观察和告知主诊医生；患者不应自行停用心脏科开的药。只就学员已得到的资料说明，不提供未记录的数据或诊断。",
                        "Reviews and fills prescriptions. Principle: the dispensary fills only the current version signed by the prescriber; any substitution or change needs a new version, and verbal changes are not accepted. Can explain that 桑寄生 and 槲寄生 come from different plants with separate Pharmacopoeia monographs — similar actions, not the same medicinal; that granules are prescribed in crude-herb equivalents; that evidence for extra bleeding with blood-activating herbs (当归, 川芎) and antiplatelets is mostly theoretical or from case reports, managed by recording, monitoring and telling the patient's doctor; and that patients must not stop medicines their cardiologist prescribed. Explains only what the learner already has; no unrecorded data or diagnosis."),
     "interprets": ["dispensary-query", "dispensing-record", "prior-records"],
     "corrections": [
         {"id": "herb-identity", "misconception": L("桑寄生和槲寄生是同一味药，可以直接互换", "桑寄生 and 槲寄生 are the same herb and can be swapped freely"),
          "match": [["槲寄生", "visci", "viscum"], ["一样", "相同", "同一", "直接换", "互换", "same", "interchangeable", "swap"]],
          "say": L("纠正一下：槲寄生和桑寄生来源不同、药典分列，是两味药。换不换由处方医师决定，而且要开新版本处方，我们才能调剂。",
                   "Correction: 槲寄生 and 桑寄生 come from different plants and have separate Pharmacopoeia monographs — they are two medicinals. Whether to swap is the prescriber's decision, and it needs a new prescription version before we can fill it."),
          "marks": ["两味药", "新版本", "different medicinal", "two medicinals", "new prescription version", "new version"]},
         {"id": "stop-aspirin", "misconception": L("服中药期间应该先停阿司匹林", "Aspirin should be stopped while herbs are taken"),
          "match": [["停", "stop", "hold", "pause"], ["阿司匹林", "aspirin"]],
          "say": L("纠正一下：他放过冠脉支架，阿司匹林不能由我们停。要调整的是中药，并且观察和告知他的心脏科医生。",
                   "Correction: he has a coronary stent, and stopping his aspirin is not ours to do. We adjust the herbs, monitor him and tell his cardiologist."),
          "marks": ["不能由我们停", "不能停", "not ours to", "must not stop", "do not stop", "don't stop"]},
     ]},
    {"role": "attending", "name": L("何医生（资深中医师）", "Dr Ho (senior TCM physician)"),
     "knowledge": L("带教的资深注册中医师，用提问引导：证据的来源、时间和质量是否可靠？支持与反对的证据各是什么？西医层面的危险信号筛查是否完整？处方改动是否留下版本记录？针灸前的同意、准备、体位是否到位？复诊时疗效不佳是辨证问题、执行问题、依从性问题，还是病情变化？不透露尚未获得的检查结果，不直接给出决策答案。",
                        "A senior registered TCM physician who teaches by asking: is the evidence's source, timing and quality trustworthy? What supports and what argues against? Is the biomedical danger-sign screen complete? Does each prescription change leave a version record? Are consent, preparation and position in place before needling? At review, is a poor response an assessment problem, an execution problem, an adherence problem or a change in the condition? Does not reveal results the learner has not obtained or give decision answers directly."),
     "interprets": ["intake-tongue-photo", "tongue-recapture", "prior-records", "dispensary-query", "dispensing-record", "acupuncture-record", "sachet-count"],
     "corrections": [
         {"id": "photo-damp-heat", "misconception": L("自助机照片上的黄苔说明是湿热", "The yellow coating on the kiosk photo means damp-heat"),
          "match": [["黄苔", "黄厚", "yellow"], ["湿热", "damp-heat", "damp heat"]],
          "say": L("纠正一下：那张照片是暖光下拍的、没有色卡，他来之前又喝过咖啡——染苔和光线都会让苔看起来发黄。先漱口、在标准光下重新看舌，再谈湿热。",
                   "Correction: that photo was taken under warm light without a colour card, and he had just drunk coffee — staining and lighting both make a coating look yellow. Have him rinse and look again under standard light before you talk about damp-heat."),
          "marks": ["染苔", "光线", "重新", "stain", "lighting", "standard light", "look again"]},
         {"id": "aspirin-no-acupuncture", "misconception": L("服阿司匹林的人不能针灸", "Patients on aspirin cannot have acupuncture"),
          "match": [["阿司匹林", "aspirin", "抗血小板", "antiplatelet"], ["不能针", "不能扎", "禁忌", "不可以针", "no acupuncture", "cannot needle", "contraindicat"]],
          "say": L("纠正一下：单用阿司匹林不是针刺的绝对禁忌。用洁净针刺技术，避开有出血风险的深刺，出针时充分按压，并观察瘀青即可。",
                   "Correction: aspirin alone is not an absolute contraindication to acupuncture. Use clean needle technique, avoid deep needling where bleeding is a concern, press well on withdrawal and watch for bruising."),
          "marks": ["不是绝对禁忌", "并非绝对禁忌", "not an absolute"]},
     ]},
    {"role": "consultant", "name": L("黄医生（综合诊所家庭医生）", "Dr Wong (polyclinic family physician)"),
     "knowledge": L("患者在综合诊所的家庭医生，可电话或书面沟通。可就腰痛危险信号、何时需要转诊或影像检查、高血压与血脂管理提供意见；强调冠脉支架术后的长期阿司匹林不能停用，需要时由心脏科决定。欢迎中医诊所告知中药与针灸方案。不掌握本次中医四诊结果，除非学员告知。",
                        "His family physician at the polyclinic, reachable by phone or letter. Can advise on back-pain danger signs, when referral or imaging is needed, and his blood pressure and lipids; stresses that long-term aspirin after a coronary stent must not be stopped, and any change is for the cardiologist. Welcomes being told about the herbal and acupuncture plan. Has none of today's TCM findings unless the learner shares them."),
     "interprets": ["prior-records"],
     "corrections": [
         {"id": "stop-aspirin-gp", "misconception": L("中药期间可以暂停阿司匹林", "Aspirin can be paused during a herbal course"),
          "match": [["停", "暂停", "stop", "hold", "pause"], ["阿司匹林", "aspirin"]],
          "say": L("纠正一下：支架术后的阿司匹林请不要停，停药会增加支架血栓的风险。需要调整的话由心脏科决定。",
                   "Correction: please do not stop his aspirin after a stent — stopping it raises the risk of stent thrombosis. Any change is for his cardiologist to decide."),
          "marks": ["不要停", "do not stop", "don't stop", "must not stop"]},
     ]},
    {"role": "receptionist", "name": L("前台", "Reception"),
     "knowledge": L("负责挂号、预约与收费（场景中的价格为虚构：初诊S$30，针灸每次S$45，配方颗粒按包计）。可提供华语、英语服务，必要时安排马来语或泰米尔语的口译。不讨论病情。",
                        "Handles registration, appointments and fees (the scenario's prices are fictional: first consultation S$30, acupuncture S$45 per session, granules charged per sachet). Serves patients in Mandarin and English and can arrange Malay or Tamil interpretation if needed. Does not discuss clinical matters."),
     "interprets": []},
]


# ---------------------------------------------------------------------------------------------
# Debrief
# ---------------------------------------------------------------------------------------------

REFERENCES = [
    "National Institute for Health and Care Excellence. Low back pain and sciatica in over 16s: assessment and management (NICE guideline NG59). London: NICE; 2016 (updated 2020).",
    "Qaseem A, Wilt TJ, McLean RM, Forciea MA; Clinical Guidelines Committee of the American College of Physicians. Noninvasive treatments for acute, subacute, and chronic low back pain: a clinical practice guideline from the American College of Physicians. Ann Intern Med. 2017;166(7):514-30.",
    "Foster NE, Anema JR, Cherkin D, Chou R, Cohen SP, Gross DP, et al. Prevention and treatment of low back pain: evidence, challenges, and promising directions. Lancet. 2018;391(10137):2368-83.",
    "World Health Organization. WHO benchmarks for the practice of acupuncture. Geneva: WHO; 2020.",
    "World Health Organization. WHO international standard terminologies on traditional Chinese medicine. Geneva: WHO; 2022.",
    "Chinese Pharmacopoeia Commission. Pharmacopoeia of the People's Republic of China, Volume I. 2020 ed. Beijing: China Medical Science Press; 2020.",
    "Traditional Chinese Medicine Practitioners Board (Singapore). Ethical code and ethical guidelines for TCM practitioners. Singapore: TCMPB.",
    "Health Sciences Authority (Singapore). Chinese proprietary medicines: overview. Singapore: HSA.",
]

DEBRIEF = {
    "title": L("复盘：一次完整的中医门诊——复发性腰痛", "Debrief: a complete TCM outpatient episode — recurrent low back pain"),
    "conclusion": L(
        "复发性非特异性腰痛，无红旗征、无神经根受累；中医诊断腰痛，证属寒湿痹阻、兼肝肾不足。关键在于：识别自助机舌象照片的染苔与光线问题并取得可靠舌象；在发药前补全用药史（阿司匹林）；把药房的缺货替换问题作为新版本处方处理，而不是口头同意；因既往晕针安排卧位，并核对进出针数；一周复诊时把依从性不足和持续诱因与辨证错误区分开——维持评估，修订的是执行方案。",
        "Recurrent non-specific low back pain with no red flags and no nerve-root involvement; TCM disease lumbago, pattern cold-damp obstruction with underlying liver–kidney insufficiency. What mattered: recognising the stained, poorly lit kiosk tongue photo and obtaining a reliable view; completing the medication history (aspirin) before supply; handling the dispensary's out-of-stock substitution as a new prescription version rather than a verbal yes; needling him lying down because he had fainted before, with needles counted in and out; and at one week, separating incomplete adherence and continuing exposure from a wrong assessment — keeping the assessment and revising how the plan is carried out.",
    ),
    "keyReasoning": [
        L("疾病与证候分两层：先用危险信号与神经系统检查回答“是否安全、是否需要转诊”，再用四诊合参回答“是什么证”。",
          "Disease and pattern are two layers: the danger-sign screen and neurological examination answer \"is it safe, does he need referral\"; the four examinations together answer \"which pattern\"."),
        L("证据有来源、时间和质量。染色、暖光、无色卡的照片不能和自然光下的直接望舌等量齐观。",
          "Evidence has a source, a time and a quality. A stained photo under warm light without a colour card does not weigh the same as direct inspection in daylight."),
        L("寒湿痹阻的依据：冷重酸痛、遇寒湿加重、得温则减、畏寒喜热饮、腰部皮温偏凉、苔白腻；肝肾不足的依据：反复发作、腰膝酸软、尺脉弱、舌淡胖有齿痕。",
          "Cold-damp obstruction: a cold, heavy ache, worse with cold and damp, better with warmth, cold intolerance, a liking for hot drinks, a cool lower back and a white greasy coating. Liver–kidney insufficiency: recurrence, sore weak knees, weak chi pulses, a pale swollen tooth-marked tongue."),
        L("处方是有版本的执行对象：提交、审核、修订、调剂、使用各留记录；药房只按现行版本发药。",
          "A prescription is an executable object with versions: submission, review, revision, dispensing and use each leave a record, and the dispensary supplies only the current version."),
        L("复诊时先核对“实际发生了什么”——发药记录、治疗记录、剩余药包——再判断疗效有限是评估问题还是执行问题。",
          "At review, first check what actually happened — the dispensing record, the session record, the sachets left — before deciding whether a limited response is an assessment problem or an execution problem."),
    ],
    "boundaries": L(
        "虚构教学病例。所给处方、取穴与疗程只是多种可辩护方案之一；其他经专家认可的方案（如以推拿或单纯运动为主）在本病例中同样不被视为错误。指南意见并不一致：美国医师协会（ACP 2017）把针灸列为慢性腰痛的非药物选择之一，而英国NICE NG59建议不提供针灸；中药治疗慢性腰痛的高质量证据有限。随访结果为编者设定，不是对真实疗效的预测。",
        "A fictional teaching case. The formula, points and course given are one defensible plan among several; other expert-endorsed plans (for example tuina or exercise-led care) are not treated as wrong here. Guidance disagrees: the American College of Physicians (2017) lists acupuncture among non-drug options for chronic low back pain, whereas NICE NG59 recommends not offering it; high-quality evidence for Chinese herbal medicine in chronic low back pain is limited. The follow-up course is authored, not a prediction of real outcomes.",
    ),
    "unknowns": [
        L("他近期的肾功能、肝功能和血常规结果。", "His recent kidney, liver and blood-count results."),
        L("所用配方颗粒产品的具体厂家、批次与监管分类（本病例产品为虚构）。", "The manufacturer, batch and regulatory class of the granule products used (fictional in this case)."),
        L("两周疗程结束后的疗效与长期复发情况。", "His response after the two-week course and his long-term recurrence."),
    ],
    "teachingPoints": [
        L("非特异性腰痛：先筛查危险信号；无红旗征时不常规做影像检查，强调保持活动与运动（NICE NG59，2016/2020更新；ACP 2017）。针灸的推荐因指南而异（ACP列为选项，NICE不推荐），知情同意时应如实说明。",
          "Non-specific low back pain: screen for danger signs first; without red flags, do not routinely image, and emphasise staying active and exercise (NICE NG59, 2016, updated 2020; ACP 2017). Guidance on acupuncture differs (an option in ACP 2017, not recommended in NICE NG59) — say so when you take consent."),
        L("舌象采集需要标准光源与色卡；问清来诊前饮食，漱口后再看——染苔是常见的证据质量陷阱。证候术语参照世卫组织中医药国际标准术语（2022）。",
          "Tongue imaging needs standard light and a colour card; ask about recent food and drink and look again after a rinse — staining is a common evidence-quality trap. Pattern terms follow the WHO international standard terminologies on TCM (2022)."),
        L("中药替换与处方变更由处方医师决定并形成新版本；桑寄生与槲寄生在《中国药典》（2020年版）中分列。完整用药史（含抗血小板药）应在调剂前取得，并与患者的主诊医生沟通。",
          "Herb substitutions and other prescription changes are the prescriber's decision and create a new version; 桑寄生 and 槲寄生 are separate monographs in the Chinese Pharmacopoeia (2020). Obtain a complete medication history, antiplatelets included, before supply, and keep the patient's own doctors informed."),
        L("针刺安全：知情同意、洁净针刺技术、一次性无菌针、锐器即时处置；有晕针史者取卧位并确认已进食；进出针数核对（参见WHO针灸实践基准，2020）。",
          "Needling safety: informed consent, clean needle technique, single-use sterile needles, immediate sharps disposal; lie down a patient who has fainted before and make sure they have eaten; count needles in and out (see the WHO benchmarks for the practice of acupuncture, 2020)."),
        L("新加坡执业：遵循中医管理委员会的伦理守则（同意、记录、转介）；产品按卫生科学局对中成药与中药材的不同规定分类。",
          "Practising in Singapore: follow the TCM Practitioners Board's ethical code (consent, records, referral); classify products under the Health Sciences Authority's separate rules for Chinese proprietary medicines and traditional medicinal materials."),
    ],
    "references": REFERENCES,
    "notice": L("评分衡量完成本教学路径的程度，未经临床能力评价验证。", "Scores measure completion of this teaching pathway and are not validated measures of clinical competence."),
}

CASE_UNKNOWNS = [
    L("近期肝肾功能与血常规结果（综合诊所去年抽血，患者不知道结果）。", "Recent liver, kidney and blood-count results (the polyclinic took blood last year; he does not know the results)."),
    L("所用颗粒产品的厂家、批号与监管分类。", "Manufacturer, batch and regulatory class of the granule products."),
    L("两周疗程后的疗效与远期复发。", "His response after two more weeks and his long-term recurrence."),
]


# ---------------------------------------------------------------------------------------------
# Reference path (cases verify replays it)
# ---------------------------------------------------------------------------------------------

def ask(*ids):
    return [{"type": "ask", "itemId": i} for i in ids]


def examine(*ids):
    return [{"type": "examine", "findingId": i} for i in ids]


def order_read(inv, phase):
    return [{"type": "order", "investigationId": inv}, {"type": "read", "investigationId": inv, "phase": phase}]


def answer(decision, *options):
    return {"type": "answer", "decisionId": decision, "optionIds": list(options)}


def intervene(*ids):
    return [{"type": "intervene", "interventionId": i} for i in ids]


SOLUTION = [
    {"type": "start"},
    *ask("h-presenting", "h-onset", "h-site", "h-character", "h-modifiers", "h-severity",
         "h-redflag-neuro", "h-redflag-ce", "h-redflag-systemic", "h-trauma",
         "h-coldheat", "h-knees-fatigue", "h-urine-stool", "h-sleep", "h-appetite", "h-food-before",
         "h-pmh", "h-meds", "h-antithrombotic", "h-herbs-supplements", "h-allergies", "h-bruising", "h-prior-acu",
         "h-occupation", "h-living", "h-smoking-alcohol", "h-exercise", "h-function", "h-family", "h-language", "h-ice"),
    *examine("e-general", "e-vitals", "e-voice-odour", "e-skin-back", "e-lumbar-palp", "e-lumbar-rom", "e-slr", "e-neuro", "e-hips", "e-abdomen", "e-pulse"),
    *order_read("intake-tongue-photo", "consult"),
    answer("d-evidence", "recheck"),
    *examine("e-tongue"),
    *order_read("tongue-recapture", "consult"),
    *order_read("prior-records", "consult"),
    answer("d-disease", "nslbp"),
    answer("d-pattern", "cold-damp"),
    # the treatment phase opens on its own once both assessments are made
    *intervene("self-management", "explain-consent", "rx-draft"),
    *order_read("dispensary-query", "treatment"),
    answer("d-rx-review", "new-version", "aspirin-managed"),
    *intervene("rx-v2-substitute", "dispense", "counsel-herbs", "gp-letter",
               "acu-prep", "acu-position", "acu-insert", "acu-remove", "acu-document", "arrange-followup"),
    # one week later: the follow-up phase opens on its own
    *ask("h-fu-status", "h-fu-adherence", "h-fu-exercise", "h-fu-adverse", "h-fu-redflags", "h-fu-other-care"),
    *examine("e-fu-lumbar", "e-fu-sites", "e-fu-neuro", "e-fu-tongue", "e-fu-pulse"),
    *order_read("dispensing-record", "followup"),
    *order_read("acupuncture-record", "followup"),
    *order_read("sachet-count", "followup"),
    answer("d-followup", "adherence"),
    *intervene("adherence-plan", "continue-course"),
    {"type": "finish"},
]


# ---------------------------------------------------------------------------------------------
# Matcher regression corpus (paraphrases; `cases verify` checks them)
# ---------------------------------------------------------------------------------------------

def U(text, locale, *expect, also=None):
    u = {"text": text, "locale": locale, "expect": list(expect)}
    if also:
        u["alsoOk"] = also
    return u


TEST_UTTERANCES = [
    U("今天怎么了，哪里不舒服？", "zh-CN", "h-presenting"),
    U("so what's the main problem today?", "en", "h-presenting"),
    U("腰痛之前有没有发作过？", "zh-CN", "h-onset"),
    U("has this happened before?", "en", "h-onset"),
    U("痛的位置具体在哪？会放射吗？", "zh-CN", "h-site"),
    U("does the pain radiate down your leg?", "en", "h-site"),
    U("是刺痛还是酸痛？", "zh-CN", "h-character"),
    U("what kind of pain is it?", "en", "h-character"),
    U("什么会让它加重？", "zh-CN", "h-modifiers"),
    U("is it worse in rainy weather?", "en", "h-modifiers"),
    U("痛得厉害吗，打几分？", "zh-CN", "h-severity"),
    U("how bad is the pain out of ten?", "en", "h-severity"),
    U("脚有没有发麻？", "zh-CN", "h-redflag-neuro"),
    U("any pins and needles in your feet?", "en", "h-redflag-neuro"),
    U("大小便能控制吗？", "zh-CN", "h-redflag-ce"),
    U("any problems with bladder control?", "en", "h-redflag-ce"),
    U("最近有发烧或者体重下降吗？", "zh-CN", "h-redflag-systemic"),
    U("any history of cancer or weight loss?", "en", "h-redflag-systemic"),
    U("你怕冷吗？", "zh-CN", "h-coldheat"),
    U("do you feel the cold easily?", "en", "h-coldheat"),
    U("晚上要起夜吗？", "zh-CN", "h-urine-stool"),
    U("来看病之前喝过咖啡吗？", "zh-CN", "h-food-before"),
    U("did you have coffee or tea this morning?", "en", "h-food-before"),
    U("你以前有什么慢性病？", "zh-CN", "h-pmh"),
    U("any past medical problems?", "en", "h-pmh"),
    U("平时吃哪些药？", "zh-CN", "h-meds"),
    U("which tablets do you take every day?", "en", "h-meds"),
    U("你有在吃阿司匹林吗？", "zh-CN", "h-antithrombotic"),
    U("are you on any blood thinners?", "en", "h-antithrombotic"),
    U("有药物过敏吗？", "zh-CN", "h-allergies"),
    U("any drug allergies?", "en", "h-allergies"),
    U("你以前扎过针吗？", "zh-CN", "h-prior-acu"),
    U("ever had acupuncture before?", "en", "h-prior-acu"),
    U("你最担心的是什么？", "zh-CN", "h-ice"),
    U("what are you most worried about?", "en", "h-ice"),
    U("家族里有人有类似的问题吗？", "zh-CN", "h-family"),
    U("这个星期有没有好一点？", "zh-CN", "h-fu-status"),
    U("颗粒有没有漏吃？", "zh-CN", "h-fu-adherence"),
    U("did you manage to take all the sachets?", "en", "h-fu-adherence"),
    U("有没有什么副作用？", "zh-CN", "h-fu-adverse"),
    U("any side effects from the treatment?", "en", "h-fu-adverse"),
    U("现在大小便正常吗，腿有没有无力？", "zh-CN", "h-fu-redflags"),
    U("any new weakness or numbness in the legs?", "en", "h-fu-redflags"),
]


# ---------------------------------------------------------------------------------------------
# The case
# ---------------------------------------------------------------------------------------------

def build() -> dict:
    return {
        "schema": "clinicalcraft/case@1",
        "id": CASE_ID,
        "version": "0.1.0",
        "title": L("腰痛反复发作 · 52岁男性", "Recurrent low back pain · 52-year-old man"),
        "summary": L("一位五十多岁的上班族来到新加坡的社区中医诊所，腰痛反复发作。完成评估与治疗，并在一周后复诊。",
                     "A working man in his fifties comes to a community TCM clinic in Singapore with back pain that keeps coming back. Assess and treat him, then see him again a week later."),
        "specialty": ["traditional-chinese-medicine", "acupuncture", "musculoskeletal"],
        "difficulty": 3,
        "setting": "outpatient",
        "facility": "tcm-sg-clinic",
        "locales": ["zh-CN", "en"],
        "estimatedMinutes": 45,
        "learningOutcomes": [
            L("筛查复发性腰痛的危险信号与神经根受累体征，并有理据地判断目前无需影像或转诊（NICE NG59）。",
              "Screen recurrent low back pain for danger signs and nerve-root involvement, and decide with reasons that imaging and referral are not needed now (NICE NG59)."),
            L("评估多模态证据的质量：识别染苔或光线不良的舌象照片，在辨证前取得可靠舌象。",
              "Judge the quality of multimodal evidence: recognise a stained or poorly lit tongue photo and obtain a reliable view before using it for pattern differentiation."),
            L("综合四诊，将寒湿痹阻兼肝肾不足与湿热、瘀血腰痛相鉴别，并说明支持与反对证据。",
              "Differentiate cold-damp obstruction with liver–kidney insufficiency from damp-heat and blood-stasis lumbago using all four examinations, stating the evidence for and against."),
            L("把药房的审方意见作为版本化的处方变更来处理，并在调剂前核实并处理同时服用的抗血小板药，与主诊医生沟通。",
              "Resolve a dispensary query as a versioned prescription change, and reconcile a concurrent antiplatelet medicine before supply, keeping the patient's doctor informed."),
            L("按知情同意、洁净针刺、防晕针体位与进出针核对的顺序安全完成一次针灸（WHO针灸实践基准）。",
              "Deliver an acupuncture session with consent, clean needle technique, a position that guards against fainting, and needles counted in and out (WHO acupuncture benchmarks)."),
            L("复诊时依据执行记录，将依从性不足与持续诱因同辨证错误区分开，不做不必要的升级处理。",
              "At review, use the execution record to separate incomplete adherence and continuing exposure from a wrong assessment, without unnecessary escalation."),
        ],
        "tags": ["tcmcraft", "singapore", "synthetic", "four-examinations", "herbal-prescribing", "acupuncture", "longitudinal"],
        "provenance": {
            "kind": "synthetic",
            "authors": ["TCMCraft contributors"],
            "license": "CC BY 4.0 (case text); see the repository for the software licence",
            "notes": L("虚构教学病例，不基于任何真实患者；人物为化名，诊所、价格与产品均为虚构。新加坡执业背景（中医管理委员会、卫生科学局分类）仅作为情境设定，不构成法规意见。",
                       "A fictional teaching case, not based on any real patient; the person is a pseudonym and the clinic, prices and products are fictional. The Singapore practice setting (TCM Practitioners Board, Health Sciences Authority classes) is context only, not regulatory advice."),
            "review": {
                "status": "unreviewed",
                "reviewedAt": "2026-11-06",
                "reviewers": [],
                "guidelines": ["NICE NG59 (2016, updated 2020)", "ACP 2017 low back pain", "WHO benchmarks for the practice of acupuncture (2020)",
                               "WHO international standard terminologies on TCM (2022)", "Chinese Pharmacopoeia 2020 ed. Vol I"],
                "notes": L("人工智能辅助编写，对照所引指南撰写，但尚未经编辑审核或执业医师审核；用于教学前请由注册中医师和家庭医生审核。",
                           "AI-assisted authoring written against the cited guidance, but not yet editorially reviewed or reviewed by a licensed clinician — have a registered TCM physician and a family physician review it before teaching use."),
            },
        },
        "disclaimer": L("虚构教学病例，不构成医疗建议；方中药物与剂量不得用于自行用药。", "Fictional teaching case — not medical advice; the herbs and doses are not for self-medication."),
        "patient": {
            "displayName": L("陈伟良（化名）", "Mr Tan Wee Liang (pseudonym)"),
            "age": 52,
            "sex": "male",
            "weightKg": 78,
            "heightCm": 170,
            "chiefComplaint": L("腰痛反复3年，此次加重3周", "Recurrent low back pain for 3 years, worse for 3 weeks"),
            "triageNote": L("52岁男性，10:20挂号，自行步入。已在候诊区完成自助问诊问卷和舌象拍照。习惯说华语，英语也可以。带来一张综合诊所的用药清单。",
                            "52-year-old man, registered at 10:20, walked in unaided. Completed the intake questionnaire and the kiosk tongue photo in the waiting area. Prefers Mandarin, comfortable in English. Brought a printout from his polyclinic."),
            "tags": [L("腰痛", "Low back pain"), L("反复发作", "Recurrent"), L("社区中医", "Community TCM")],
            "persona": {
                "personality": L("务实、讲道理的中年主管，工作忙，有点担心但愿意配合；不喜欢多吃西药。",
                                 "A practical, reasonable supervisor in his fifties — busy, a little worried, willing to cooperate; would rather not take more Western pills."),
                "speechStyle": L("华语为主，偶尔夹一两个英文词或新加坡口语，句子短，直来直去。",
                                 "Mostly Mandarin with the odd English word or Singapore turn of phrase; short, direct sentences. In English he speaks plain Singapore English."),
                "healthLiteracy": "medium",
                "affect": "in-pain",
                "openingLine": L("医生你好。我腰又痛了，这次三个星期还没好，想看看中医有没有办法。",
                                 "Hello, doctor. My back's playing up again — three weeks now and it's not settling, so I thought I'd see what TCM can do."),
                "fallbackUnknown": L("这个我不太清楚，医生。", "I'm not sure about that, doctor."),
                "concerns": [
                    L("是不是椎间盘突出？会不会要开刀？", "Is it a slipped disc? Will I need an operation?"),
                    L("中药会不会跟我的心脏药冲突？", "Will the herbs clash with my heart medicine?"),
                    L("要来几次？我还要上班的。", "How many times must I come? I still have to work."),
                ],
                "actingNotes": L("腰部僵硬，坐下站起都慢，动作谨慎。被问到用药时只说血压药和胆固醇药，直到被具体问到阿司匹林或“血稀”的药才想起来。对再次针灸有点紧张，主动提出要躺着扎。只陈述病例中有的内容。",
                                 "Stiff in the back, slow and careful getting up and sitting down. Asked about medicines, he names only the blood-pressure and cholesterol pills until asked specifically about aspirin or blood thinners. A little nervous about acupuncture after last time, and asks to lie down for it. States only what the case contains."),
            },
            "appearance": {"skin": "#d9b38c", "hair": "#2b2622", "hairStyle": "short", "shirt": "#5b7fa3", "pants": "#3a3f4a", "build": "heavy", "stature": "adult", "gown": False, "accessory": "glasses"},
            "posture": "sitting",
        },
        "phases": PHASES,
        "initialPhase": "consult",
        "clock": {"mode": "static", "realtimeScale": 0},
        "history": HISTORY,
        "exam": EXAM,
        "examNotRecorded": L("本病例中没有这项检查的结果。", "This examination has no result in this case."),
        "investigations": INVESTIGATIONS,
        "orderMatching": ORDER_MATCHING,
        "interventions": INTERVENTIONS,
        "objectives": OBJECTIVES,
        "decisions": DECISIONS,
        "rubric": RUBRIC,
        "npcs": NPCS,
        "debrief": DEBRIEF,
        "safetyGates": SAFETY_GATES,
        "unknowns": CASE_UNKNOWNS,
        "solution": SOLUTION,
        "extensions": {
            "testUtterances": TEST_UTTERANCES,
            "tcmcraft": {
                "edition": "singapore",
                "modules": ["four-examinations", "pattern-differentiation", "herbal-prescribing", "acupuncture", "care-coordination", "longitudinal-follow-up"],
                "patternFramework": "zang-fu and bi-syndrome (脏腑辨证 · 痹证辨证)",
                "acceptablePathways": [
                    {"id": "substitute", "decisionPoint": "dispensary-query", "interventions": ["rx-v2-substitute", "dispense"],
                     "rationale": "Prescriber names 槲寄生 in a new signed version."},
                    {"id": "omit", "decisionPoint": "dispensary-query", "interventions": ["rx-v2-omit", "dispense"],
                     "rationale": "Prescriber leaves 桑寄生 out in a new signed version; 杜仲 and 牛膝 remain."},
                    {"id": "tuina-adjunct", "decisionPoint": "treatment", "interventions": ["tuina"],
                     "rationale": "Tuina as an adjunct after consent is acceptable and not required."},
                ],
                "unacceptable": ["rx-verbal-swap", "stop-aspirin", "switch-damp-heat", "double-dose"],
                "expertDisagreement": [
                    "Whether 当归 and 川芎 should be kept at usual doses or removed alongside aspirin (both accepted).",
                    "Whether the underlying deficiency is best framed as liver–kidney or spleen–kidney (both reasoned; the rubric scores the cold-damp primary pattern).",
                ],
                "evidence": {
                    "intake-tongue-photo": {"source": "self-service kiosk", "quality": "failed colour check", "confounders": ["warm light", "no colour card", "recent coffee"]},
                    "tongue-recapture": {"source": "tongue-imaging station", "quality": "passed"},
                    "e-tongue": {"source": "direct inspection after rinsing, daylight"},
                    "e-pulse": {"source": "clinician palpation (authored description, no waveform)"},
                },
                "followUpModel": "authored branch (not a calibrated outcome model)",
            },
        },
    }
