"""Case tcm-sg-lbp-04 — family sg-lbp, review D: the pattern has changed by the one-week review.

The first visit is tcm-sg-lbp-01's, unchanged. Over the week he took every sachet of the warming formula, wore a heat
patch all day, every day, took very hot showers, and ate durian twice with beer and fried food at a wedding. The cold,
heavy ache has become a hot, heavy, distending pain that is worse in the heat. He now feels the heat, has a bitter,
sticky mouth, darker urine and sticky stools. Seen after a rinse in daylight, and under the standard light, the tongue
has red edges and a thin yellow greasy coating at the root: this time the yellow is real. His pulse is slippery and
slightly rapid. There is no fever and no urinary or loin symptoms, and the neurological examination is normal.

Cold-damp has transformed into damp-heat. The plan changes: stop the warming formula and the heat patches (which have
reddened his skin), issue prescription version 3 to clear heat and drain damp, give diet advice, and review again.

Phase 2 dimension: a follow-up branch with a changed condition, so the assessment is revised (DESIGN §3 contribution
4). It is also the evidence-quality inversion of the first visit: the discipline that set aside a stained coating
accepts a genuine one.
"""

from __future__ import annotations

import copy

import case_lbp as base
import lbp_family
from case_lbp import AUTHORED, FOLLOWUP, KW, L, U, answer, ask, ex, examine, hx, intervene, iv, opt, order_read
from common import dates

CASE_ID = "tcm-sg-lbp-04"

HISTORY = [
    hx("h-fu-status", "hpi",
       L("这一个星期腰怎么样了？", "How has your back been this past week?"),
       L("没那么冷痛了，可是这几天变成热热的、胀胀的痛，下午更明显。洗热水澡反而更难受，冲凉水还舒服一点。现在大概五分。",
         "It isn't the cold ache any more — these last few days it's a hot, heavy, swollen sort of pain, worse in the afternoon. Hot showers make it worse now; a cool rinse feels better. About a five."),
       KW(["这个星期", "这一周", "这周", "好点了吗", "有没有好转", "上次以后", "有什么变化"],
          ["this week", "past week", "improved", "any better", "progress", "since last time", "changed"]),
       required=True, phases=FOLLOWUP, supersedes=["h-presenting", "h-severity", "h-character"]),
    hx("h-fu-heat", "associated-symptoms",
       L("现在怕冷还是怕热？口干口苦吗？", "Do you feel the heat or the cold more now, and is your mouth dry or bitter?"),
       L("现在反而怕热，身上黏黏的。早上起来嘴巴苦苦的、黏黏的，会口渴，可是喝不了多少。",
         "I feel the heat more now, and sticky all over. I wake with a bitter, sticky mouth; I'm thirsty but can't drink much."),
       KW(["口苦", "口干", "嘴巴苦", "现在怕热", "身上黏"], ["bitter", "bitter taste", "sticky mouth", "feel the heat now"]),
       required=True, phases=FOLLOWUP, supersedes=["h-coldheat", "h-appetite"]),
    hx("h-fu-urine-stool", "associated-symptoms",
       L("这几天小便、大便怎么样？", "What have your urine and stools been like these last few days?"),
       L("小便比较黄，量少一点，没有痛也没有烧的感觉；大便黏黏的，冲不干净。",
         "My urine's darker and there's less of it, but it doesn't hurt or burn; my stools are sticky and hard to flush."),
       KW(["这几天小便", "这几天大便", "大便黏"], ["stools sticky", "urine darker"]),
       phases=FOLLOWUP, supersedes=["h-urine-stool"]),
    hx("h-fu-fever", "ros",
       L("有没有发烧、发冷或出汗？腰两侧或小便时痛不痛？", "Any fever, chills or sweats, or pain in your sides or when you pass urine?"),
       L("没有发烧，也没有发冷、出汗。腰两边侧面不痛，小便也不痛。体重没变。", "No fever, no chills or sweats. No pain in my sides, and passing water doesn't hurt. My weight's the same."),
       KW(["发烧", "发冷", "出汗", "腰两侧", "小便痛", "尿痛"], ["fever", "chills", "sweats", "pain on passing urine", "loin pain", "flank"]),
       required=True, phases=FOLLOWUP, supersedes=["h-redflag-systemic"]),
    hx("h-fu-diet", "other",
       L("这个星期吃喝了些什么？今天来之前吃了什么？", "What have you been eating and drinking this week, and what did you have before coming today?"),
       L("朋友请吃榴莲，这个星期吃了两次，还喝了几罐啤酒，在婚宴上也吃了不少炸的。今天来之前只吃了白粥、喝了水，没喝咖啡。",
         "Friends treated me to durian — twice this week — and I had a few beers, plus lots of fried food at a wedding dinner. Before coming today I only had plain porridge and water; no coffee."),
       KW(["吃了些什么", "吃些什么", "饮食", "榴莲", "吃炸的", "来之前吃"], ["diet", "durian", "fried food", "eating lately", "before coming today"]),
       disclosure="specific", phases=FOLLOWUP, supersedes=["h-food-before"]),
    hx("h-fu-heat-patches", "other",
       L("暖贴和热水澡还在用吗？", "Have you still been using the heat patches and hot showers?"),
       L("有，每天贴暖贴，一贴就是一整天，还洗很烫的热水澡。我想暖一点会好得快。",
         "Yes — a heat patch every day, all day long, and very hot showers. I thought warmer would get me better faster."),
       KW(["暖贴", "热水澡", "贴多久", "还在贴"], ["patches", "hot showers", "still using", "allday"]),
       disclosure="specific", phases=FOLLOWUP),
    hx("h-fu-adherence", "medications",
       L("颗粒冲剂有没有按时吃？", "Have you been taking the granules as we agreed?"),
       L("有，早晚各一包，一包都没漏。", "Yes — one morning and evening, not a single one missed."),
       KW(["按时吃", "有没有吃药", "颗粒", "冲剂", "漏吃", "忘了吃", "中药吃了吗"],
          ["granules", "sachets", "taking the herbs", "missed doses", "missed any", "adherence", "remember to take"]),
       phases=FOLLOWUP),
    hx("h-fu-adverse", "other",
       L("治疗以后有没有什么不舒服或者副作用？", "Any side effects or problems since the treatment?"),
       L("没有瘀青或出血。倒是腰上贴暖贴的地方有点红、有点痒。", "No bruising or bleeding. But the skin where I put the heat patches is a bit red and itchy."),
       KW(["副作用", "不良反应", "治疗以后", "皮肤红", "痒"], ["side effects", "sideeffects", "problems since", "skin red", "itchy"]),
       phases=FOLLOWUP, supersedes=["h-bruising"]),
    hx("h-fu-redflags", "ros",
       L("现在腿脚有没有麻木无力？大小便控制得住吗？", "Any numbness or weakness in your legs now, and can you control your bladder and bowels?"),
       L("都没有，腿不麻，也有力气，大小便都控制得住。", "None of that — my legs are fine, no numbness, and I've full control down below."),
       KW(["现在腿", "现在有没有麻", "新的麻木"], ["new weakness", "new numbness", "newnumbness"]),
       required=True, phases=FOLLOWUP, supersedes=["h-redflag-neuro", "h-redflag-ce"]),
]

EXAM = [
    ex("e-fu-vitals", "vitals",
       L("测量体温、脉率与血压", "Measure temperature, pulse rate and blood pressure"),
       L("体温36.8℃，脉率86次/分，血压134/82 mmHg。", "Temperature 36.8 °C, pulse 86/min, blood pressure 134/82 mmHg."),
       KW(["体温", "量体温", "生命体征", "血压"], ["temperature", "vital signs", "vitals", "blood pressure"]),
       required=True, phases=FOLLOWUP),
    ex("e-fu-tongue", "heent",
       L("复查舌象（漱口后、自然光下）", "Re-inspect the tongue (rinsed, in daylight)"),
       L("舌边红，舌根部苔薄黄腻；漱口后颜色不退。", "Tongue edges red; a thin yellow greasy coating at the root that does not change after rinsing."),
       KW(["舌", "舌象", "舌苔", "望舌"], ["tongue", "coating", "inspect the tongue"]),
       abnormal=True, required=True, phases=FOLLOWUP),
    ex("e-fu-pulse", "cardiovascular",
       L("复诊切脉", "Retake the pulse"),
       L("脉滑略数，86次/分，节律齐。", "Slippery and slightly rapid, 86/min, regular."),
       KW(["切脉", "把脉", "脉象", "号脉"], ["pulse", "radial pulse", "take the pulse"]),
       abnormal=True, required=True, phases=FOLLOWUP),
    ex("e-fu-lumbar", "musculoskeletal",
       L("复查腰部压痛、皮温与活动度", "Re-examine lumbar tenderness, skin temperature and range of movement"),
       L("右侧L4–S1椎旁压痛；腰部皮温较上周偏温；前屈指尖达踝部。", "Right L4–S1 paravertebral tenderness; the lower back now warm to touch rather than cool; flexion to fingertips at the ankles."),
       KW(["复查腰部", "腰部压痛", "活动度", "皮温", "触诊腰部"], ["re-examine the back", "tenderness", "range of movement", "skin temperature", "palpate"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-skin", "skin",
       L("查看腰背部皮肤（贴暖贴处）", "Inspect the skin of the lower back where the heat patches were worn"),
       L("腰部两处约5 cm的淡红斑，皮温稍高，无水疱、无破损。", "Two faint red patches about 5 cm across over the lower back, slightly warm, with no blisters or broken skin."),
       KW(["皮肤", "腰背部皮肤", "暖贴处", "红斑"], ["skin", "skin of the back", "patch sites", "redness"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-renal", "abdomen",
       L("双侧肾区叩击", "Percuss both renal angles"),
       L("双侧肾区叩击痛阴性。", "Percussion over both renal angles is painless."),
       KW(["肾区叩击", "肾区", "叩击痛"], ["renal angle", "renal angles", "loin percussion", "costovertebral"]),
       phases=FOLLOWUP),
    ex("e-fu-neuro", "neurological",
       L("复查双下肢神经系统与直腿抬高", "Repeat the lower-limb neurological check and straight-leg raise"),
       L("肌力、反射与轻触觉均正常，与上周一致；直腿抬高双侧80°，无下肢痛。",
         "Power, reflexes and light touch normal and unchanged from last week; straight-leg raise 80° on both sides without leg pain."),
       KW(["神经系统", "肌力", "反射", "直腿抬高", "感觉"], ["neuro", "neurological", "power", "reflexes", "straight leg raise"]),
       phases=FOLLOWUP, requires=["reflex-hammer"]),
]

# the standard tongue capture, now also available at the review
TONGUE_RECAPTURE = copy.deepcopy(next(i for i in base.INVESTIGATIONS if i["id"] == "tongue-recapture"))
TONGUE_RECAPTURE["results"]["followup"] = {
    "date": L("今日复诊", "Today's review"),
    "text": L("漱口后在标准环形光源下拍摄，色卡在画面内，质量校验通过：舌边红，舌根部苔薄黄腻；舌下络脉无明显迂曲。",
              "Taken after a rinse, under the standard ring light with the colour card in frame; quality check passed: tongue edges red, a thin yellow greasy coating at the root; sublingual veins not distended."),
    "note": L("与初诊时的标准采集相比，苔由白腻转为黄腻。", "Compared with the standard capture at the first visit, the coating has turned from white and greasy to yellow and greasy."),
    "source": AUTHORED,
}

INVESTIGATIONS = [
    TONGUE_RECAPTURE,
    {
        "id": "sachet-count",
        "name": L("清点剩余颗粒药包并核对服药记录", "Count the remaining granule sachets and check his dose diary"),
        "category": "bedside",
        "aliases": KW(["清点药包", "剩余药包", "数药包", "服药记录", "服药日记"], ["count sachets", "sachet count", "remaining sachets", "pill count", "dose diary"]),
        "risk": "none",
        "performedAt": "bedside",
        "value": "useful",
        "results": {
            "followup": {
                "date": L("今日复诊", "Today's review"),
                "text": L("14包全部服完，服药记录每天早晚各一包。", "All 14 sachets taken; the dose diary shows one each morning and evening."),
                "source": AUTHORED,
            }
        },
    },
]

FORMULA_ZH = (
    "第3版处方（第2版作废）：四妙丸加减配方颗粒，以饮片当量计（克/日）：苍术9、黄柏9、牛膝10、薏苡仁30、秦艽9、忍冬藤15。"
    "每日1剂分2包，每次1包，每日2次，饭后温水冲服，共7天（14包）。用药记录照旧包括阿司匹林100 mg。"
)
FORMULA_EN = (
    "Prescription version 3 (version 2 cancelled): modified Si Miao Wan (四妙丸) as concentrated granules, in crude-herb equivalents (g/day): "
    "苍术 Atractylodis Rhizoma 9, 黄柏 Phellodendri Chinensis Cortex 9, 牛膝 Achyranthis Bidentatae Radix 10, 薏苡仁 Coicis Semen 30, "
    "秦艽 Gentianae Macrophyllae Radix 9, 忍冬藤 Lonicerae Japonicae Caulis 15. One day's dose in 2 sachets: 1 sachet twice daily after meals in warm water, "
    "for 7 days (14 sachets). The medication record still includes aspirin 100 mg."
)

REVIEW_ONLY = {"not": {"phase": "followup"}}

INTERVENTIONS = [
    iv("rx-v3-damp-heat", "medication",
       L("开具处方第3版：清热利湿（四妙丸加减），第2版作废", "Issue prescription version 3 to clear heat and drain damp (modified 四妙丸), cancelling version 2"),
       KW(["四妙丸", "清热利湿", "处方第3版", "改方", "湿热方"], ["si miao", "clear heat", "prescription version 3", "damp-heat formula", "switch formula"]),
       dose=L(FORMULA_ZH, FORMULA_EN),
       requires=["records"], scope="medical", risk="low", checklist=True, maxDoses=1, setFlags=["rx-v3"],
       contraindicatedWhen=REVIEW_ONLY,
       harm=L("初诊时的证据支持寒湿：此时用苦寒清热之品会伤阳，加重寒湿。",
              "At the first visit the evidence supports cold-damp: bitter-cold, heat-clearing herbs now would injure yang and make the cold-damp worse."),
       indicatedWhen={"decided": "d-followup"},
       response=L("第3版处方已签发，药房确认第2版作废。", "Version 3 is signed; the dispensary confirms version 2 is cancelled.")),
    iv("dispense-v3", "medication",
       L("将第3版处方交药房调剂并发药", "Release prescription version 3 for dispensing and supply"),
       KW(["发药", "调剂", "配药", "取药", "第3版发药"], ["dispense", "supply", "fill the new prescription", "dispense version 3"]),
       requires=["medications"], risk="low", checklist=True, maxDoses=1, setFlags=["dispensed-v3"],
       contraindicatedWhen={"not": {"intervened": "rx-v3-damp-heat", "valid": True}},
       harm=L("还没有新的处方版本可以发。", "There is no new prescription version to supply yet."),
       response=L("药房按第3版调剂了14包，标签与处方核对一致。", "The dispensary fills 14 sachets from version 3; the label is checked against the prescription.")),
    iv("stop-heat", "other",
       L("停用暖贴和过烫的热水澡，让发红的皮肤恢复", "Stop the heat patches and very hot showers, and let the reddened skin recover"),
       KW(["停暖贴", "不要贴暖贴", "别洗太烫", "停热敷"], ["stop the patches", "no more heat patches", "cooler showers", "stop heat"]),
       risk="none", checklist=True, setFlags=["heat-stopped"],
       contraindicatedWhen=REVIEW_ONLY,
       harm=L("初诊时他是寒湿，局部温热正合适。", "At the first visit, with cold-damp, local warmth is appropriate."),
       indicatedWhen={"asked": "h-fu-heat-patches"},
       response=L("他把剩下的暖贴收了起来：“原来不是越热越好。”", "He puts the remaining patches away: \"So warmer isn't always better.\"")),
    iv("diet-advice", "other",
       L("饮食建议：暂时不吃榴莲、不喝酒、少吃油炸厚味，清淡饮食，适量饮水", "Diet advice: no durian or alcohol for now, less fried and rich food, plain meals and enough water"),
       KW(["饮食建议", "忌口", "少吃油炸", "不吃榴莲", "戒酒"], ["diet advice", "avoid durian", "less fried food", "no alcohol", "whattoeat"]),
       risk="none", checklist=True, setFlags=["diet-advised"],
       contraindicatedWhen=REVIEW_ONLY,
       harm=L("初诊时还没有需要特别忌口的情况。", "At the first visit there is nothing in particular to avoid."),
       response=L("他苦笑：“榴莲季节刚到……好吧。”", "He grimaces: \"Just when durian season starts… all right.\"")),
    iv("continue-course", "disposition",
       L("维持第2版处方与既定疗程不变", "Keep prescription version 2 and the planned course unchanged"),
       KW(["继续治疗", "继续疗程", "维持方案", "原方继续"], ["continue treatment", "continue the course", "carry on", "same formula"]),
       risk="low", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("证候已经变了：继续温经散寒的方子会继续助热，加重湿热。", "The pattern has changed: carrying on with a warming formula keeps adding heat and makes the damp-heat worse."),
       response=L("下次预约已排好。", "The next appointments are booked.")),
    iv("add-fuzi", "medication",
       L("加附子以加强温阳散寒", "Add processed aconite (附子) to strengthen the warming"),
       KW(["加附子", "附子", "温阳", "加强温热"], ["aconite", "fu zi", "add fuzi", "more warming"]),
       scope="medical", risk="high", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("已有热象时再加大热有毒的附子，是火上加油；附子含乌头类生物碱，过量或煎煮不当可致心律失常，必须有明确指征并先煎久煎。",
              "Adding aconite — very hot and toxic — when there are already heat signs adds fuel to the fire. It contains aconite alkaloids that can cause arrhythmia in overdose or when poorly prepared; it needs a clear indication and long prior decoction."),
       response=L("处方已改。", "The prescription is changed.")),
]

DECISIONS = [
    {
        "id": "d-followup", "kind": "single",
        "prompt": L("一周后，他的症状、舌象与脉象都变了。现在的评估与处理是什么？", "A week on, his symptoms, tongue and pulse have changed. What is your assessment and plan now?"),
        "requires": {"all": [{"asked": "h-fu-status"}, {"asked": "h-fu-heat"}, {"asked": "h-fu-fever"}, {"examined": "e-fu-vitals"}, {"examined": "e-fu-pulse"},
                             {"any": [{"examined": "e-fu-tongue"}, {"read": "tongue-recapture", "phase": "followup"}]}]},
        "need": L("先问清楚这一周的变化、寒热与口味、有无发热及泌尿症状，测体温，并复查舌脉。",
                  "First ask how things have changed this week, about heat or cold and his mouth, and about fever and urinary symptoms; take his temperature, and re-examine the tongue and pulse."),
        "options": [
            opt("heat", True,
                L("寒湿化热，转为湿热（温热药、整天贴暖贴、天气炎热加上榴莲、啤酒和油炸食物）；无发热等危险信号——停温热方与暖贴，开具清热利湿的新版本处方，饮食建议，一周后再评估",
                  "Cold-damp has transformed into damp-heat (a warming formula, all-day heat patches, hot weather, durian, beer and fried food); no fever or other danger signs — stop the warming formula and the heat patches, issue a new prescription version that clears heat and drains damp, give diet advice, and review in a week"),
                L("正确。热痛、遇热加重、得凉则舒、口苦黏、尿黄、便黏、舌边红苔黄腻（漱口、自然光与标准光源下一致）、脉滑数，都指向湿热。证候会随治疗、饮食与季节变化，每次复诊都要重新辨证。",
                  "Correct. A hot pain worse with heat and better with cool, a bitter sticky mouth, dark urine, sticky stools, red tongue edges with a yellow greasy coating (consistent after a rinse, in daylight and under standard light), and a slippery, rapid pulse all point to damp-heat. Patterns change with treatment, diet and season, so re-differentiate at every review.")),
            opt("staining", False,
                L("黄苔又是染苔，维持原方", "The yellow coating is staining again: keep the current formula"),
                L("不对。这次他漱过口、今天没喝咖啡，在自然光和标准光源下看都是黄腻苔，而且与症状、脉象一致。证据质量的标准对两个方向都适用：可靠的证据就要采信。",
                  "No. This time he rinsed and had no coffee today, and the coating is yellow and greasy in daylight and under standard light — and it agrees with his symptoms and pulse. Evidence-quality standards cut both ways: reliable evidence has to be accepted.")),
            opt("infection", False,
                L("腰部热痛加黄苔，是脊柱感染，应转急诊", "Hot back pain with a yellow coating means a spinal infection: send him to the Emergency Department"),
                L("不对。排查感染是对的，但他体温36.8℃，没有寒战、出汗、体重下降或泌尿症状，肾区叩击痛阴性，神经系统正常。没有危险信号就不升级。",
                  "No. Checking for infection was right, but his temperature is 36.8 °C, with no chills, sweats, weight loss or urinary symptoms, painless renal angles and a normal neurological examination. Without danger signs, there is no escalation.")),
            opt("more-warming", False,
                L("温热不够，加附子加强温阳", "Not warm enough: add aconite to push the warming"),
                L("不对。已有热象再加大热有毒的附子，只会加重湿热，还增加乌头碱中毒风险。",
                  "No. Adding very hot, toxic aconite to existing heat signs only worsens the damp-heat and adds the risk of aconite poisoning.")),
            opt("stay", False,
                L("中药需要时间，维持原方原疗程", "Herbs take time: keep the same formula and course"),
                L("不对。问题不是时间不够，而是证候已经变了；继续温热方会继续助热。",
                  "No. The problem is not too little time but a changed pattern; carrying on with the warming formula keeps adding heat.")),
        ],
    }
]

OBJECTIVES = [
    {"id": "o-followup", "title": L("一周复诊：重新辨证并修订方案", "One-week review: re-differentiate the pattern and revise the plan"),
     "short": L("复诊", "Review"),
     "hint": L("像初诊一样把四诊重新做一遍，也重新判断每条证据是否可靠；排除危险信号后，再看方案哪些地方需要改。",
               "Repeat the four examinations as at the first visit, judging again how far each piece of evidence can be trusted; once danger signs are excluded, decide what in the plan has to change."),
     "guidance": L("在诊室与陈先生复诊。", "Review Mr Tan in the consulting room."),
     "completeWhen": {"all": [{"decided": "d-followup"}, {"intervened": "dispense-v3", "valid": True}, {"intervened": "stop-heat", "valid": True}, {"intervened": "diet-advice", "valid": True}]},
     "waypoints": [{"target": "patient"}]},
]

MORE_WARMING = ["continue-course", "add-fuzi"]

RUBRIC = [
    {"id": "r-review-inquiry", "domain": "history", "weight": 3,
     "text": L("复诊时重新问寒热、口味、二便、发热与泌尿症状、饮食和暖贴使用", "At review, asked again about heat and cold, taste, urine and stools, fever and urinary symptoms, diet and the heat patches"),
     "met": {"all": [{"asked": h} for h in ["h-fu-heat", "h-fu-urine-stool", "h-fu-fever", "h-fu-diet", "h-fu-heat-patches"]]}},
    {"id": "r-review-exam", "domain": "examination", "weight": 2,
     "text": L("复诊时测体温，复查舌脉，查看暖贴处皮肤并叩击肾区", "At review, took his temperature, re-examined the tongue and pulse, inspected the skin under the patches and percussed the renal angles"),
     "met": {"all": [{"examined": "e-fu-vitals"}, {"examined": "e-fu-pulse"}, {"examined": "e-fu-skin"}, {"examined": "e-fu-renal"},
                     {"any": [{"examined": "e-fu-tongue"}, {"read": "tongue-recapture", "phase": "followup"}]}]}},
    {"id": "r-revise", "domain": "diagnosis", "weight": 3, "critical": True,
     "text": L("首次即识别寒湿化热并修订评估", "Recognised that cold-damp had turned to damp-heat and revised the assessment, first time"),
     "met": {"decidedFirstTry": "d-followup"}},
    {"id": "r-new-version", "domain": "safety", "weight": 3,
     "text": L("以新的处方版本替代，并只按现行版本发药", "Replaced the formula with a new prescription version and supplied only the current version"),
     "met": {"intervened": "dispense-v3", "valid": True}},
    {"id": "r-stop-heat", "domain": "safety", "weight": 2,
     "text": L("停用整天贴的暖贴与过烫热水澡（皮肤已发红）", "Stopped the all-day heat patches and very hot showers (the skin was already red)"),
     "met": {"intervened": "stop-heat", "valid": True}},
    {"id": "r-diet", "domain": "management", "weight": 1,
     "text": L("给予饮食建议", "Gave diet advice"),
     "met": {"intervened": "diet-advice", "valid": True}},
    {"id": "r-no-more-warming", "domain": "safety", "weight": 2,
     "text": L("没有继续温热方或加用附子", "Did not carry on with the warming formula or add aconite"),
     "met": {"not": {"any": [{"intervened": x} for x in MORE_WARMING]}},
     "scoredWhen": {"any": [{"phase": "followup"}] + [{"intervened": x} for x in MORE_WARMING]}},
    {"id": "r-comm-change", "domain": "communication", "weight": 1,
     "text": L("向他说明证候为什么变了、方案为什么要改，并不带评判地讨论饮食", "Explained why the pattern has changed and why the plan must change, and discussed diet without judgement"),
     "judgeGuidance": L("学员是否用通俗的话说明身体的“寒”已转为“湿热”、这不等于上次治疗错了、暖贴为什么要停（皮肤已发红，有低温烫伤风险），并不带指责地讨论榴莲、啤酒与油炸食物，与他商量可行的饮食？",
                        "Did the learner explain in plain words that the body's \"cold\" has turned to \"damp-heat\", that this does not mean last week's treatment was wrong, why the heat patches must stop (the skin is red, with a risk of a low-temperature burn), and discuss durian, beer and fried food without blame, agreeing a diet he can keep?")},
]

SAFETY_GATES = [
    {"id": "g-aconite-into-heat", "verdict": "safety-critical", "capPercent": 40,
     "label": L("在已有热象时加用附子", "Aconite added despite established heat signs"),
     "when": {"intervened": "add-fuzi"}},
    {"id": "g-revision-intercepted", "verdict": "complication",
     "label": L("在有依据之前尝试改用清热方（已被拦截）", "A heat-clearing formula attempted before there was evidence for it (intercepted)"),
     "when": {"intervened": "rx-v3-damp-heat", "valid": False}},
]

SOLUTION = [
    *ask("h-fu-status", "h-fu-heat", "h-fu-urine-stool", "h-fu-fever", "h-fu-diet", "h-fu-heat-patches", "h-fu-adherence", "h-fu-adverse", "h-fu-redflags"),
    *examine("e-fu-vitals", "e-fu-tongue", "e-fu-pulse", "e-fu-lumbar", "e-fu-skin", "e-fu-renal", "e-fu-neuro"),
    *order_read("tongue-recapture", "followup"),
    *order_read("sachet-count", "followup"),
    answer("d-followup", "heat"),
    *intervene("stop-heat", "diet-advice", "rx-v3-damp-heat", "dispense-v3"),
    {"type": "finish"},
]

UTTERANCES = [
    U("这一周腰痛有什么变化？", "zh-CN", "h-fu-status"),
    U("has the pain changed this week?", "en", "h-fu-status"),
    U("现在怕热还是怕冷？", "zh-CN", "h-fu-heat"),
    U("is there a bitter taste in your mouth?", "en", "h-fu-heat"),
    U("有没有发烧？", "zh-CN", "h-fu-fever"),
    U("any fever or chills?", "en", "h-fu-fever"),
    U("最近吃了些什么？", "zh-CN", "h-fu-diet"),
    U("have you had durian or fried food lately?", "en", "h-fu-diet"),
    U("还在贴暖贴吗？", "zh-CN", "h-fu-heat-patches"),
    U("are you still using those patches?", "en", "h-fu-heat-patches"),
    U("现在腿有没有麻、没力气？", "zh-CN", "h-fu-redflags"),
    U("any new weakness or numbness in the legs?", "en", "h-fu-redflags"),
]

OUTCOME = L("复诊时依据一致且质量可靠的证据识别证候已变（寒湿化热），排除感染等危险信号，停止助热的做法并开具新版本处方。",
            "At review, recognise from consistent, good-quality evidence that the pattern has changed (cold-damp turning to damp-heat), exclude infection and other danger signs, stop what is adding heat and issue a new prescription version.")

DEBRIEF = {
    "title": L("复盘：复发性腰痛——复诊时证候已变", "Debrief: recurrent low back pain — the pattern has changed by the review"),
    "conclusion": L(
        "初诊同 tcm-sg-lbp-01。一周后，温热方、整天贴暖贴、过烫热水澡，加上炎热天气里的榴莲、啤酒与油炸食物，使寒湿化热：热痛、遇热加重、口苦黏、尿黄、便黏、舌边红苔黄腻、脉滑数。体温正常，无泌尿或全身症状，神经系统正常。评估要改：停温热方和暖贴（皮肤已发红），开具第3版处方清热利湿，饮食建议，一周后再评估。",
        "First visit as in tcm-sg-lbp-01. A week of the warming formula, all-day heat patches and very hot showers, with durian, beer and fried food in hot weather, has turned cold-damp into damp-heat: a hot pain worse with heat, a bitter sticky mouth, dark urine, sticky stools, red tongue edges with a yellow greasy coating and a slippery, rapid pulse. His temperature is normal, with no urinary or systemic symptoms and a normal neurological examination. The assessment changes: stop the warming formula and the heat patches (the skin is already red), issue prescription version 3 to clear heat and drain damp, give diet advice, and review in a week.",
    ),
    "keyReasoning": base.DEBRIEF["keyReasoning"][:4] + [
        L("证候会随治疗、饮食与季节变化：每次复诊都重新四诊合参。判断证据质量的标准对两个方向都适用——初诊时排除染色的黄苔，复诊时就要采信漱口后、标准光源下仍为黄色的苔。",
          "Patterns change with treatment, diet and season: repeat the four examinations at every review. The evidence-quality standard cuts both ways — the discipline that set aside a stained yellow coating at the first visit accepts one that stays yellow after a rinse and under standard light."),
    ],
    "teachingPoints": base.DEBRIEF["teachingPoints"] + [
        L("寒湿日久或过用温燥可化热：复诊时如出现热痛、口苦、尿黄、舌红苔黄腻、脉滑数，应先排除感染等危险信号，再修订处方并去除助热因素（暖贴、热饮、辛辣油炸、酒）。暖贴整天贴敷可致低温烫伤。",
          "Cold-damp can turn to heat over time or with too much warming: if a review brings hot pain, a bitter taste, dark urine, a red tongue with a yellow greasy coating and a slippery, rapid pulse, exclude infection and other danger signs first, then revise the prescription and remove what adds heat (heat patches, hot drinks, spicy and fried food, alcohol). Heat patches worn all day can cause low-temperature burns."),
    ],
}


def build() -> dict:
    return lbp_family.variant(
        case_id=CASE_ID,
        version="0.2.0",
        variant_id="review-d-changed-pattern",
        title=L("腰痛反复发作 · 52岁男性 · 复诊D", "Recurrent low back pain · 52-year-old man · review D"),
        outcome=OUTCOME,
        review={"history": HISTORY, "exam": EXAM, "investigations": INVESTIGATIONS, "interventions": INTERVENTIONS, "decisions": DECISIONS,
                "objectives": OBJECTIVES, "rubric": RUBRIC, "safetyGates": SAFETY_GATES, "solution": SOLUTION, "utterances": UTTERANCES},
        debrief=DEBRIEF,
        tcmcraft={
            "dates": dates("2026-11-07"),
            "unacceptable": ["rx-verbal-swap", "stop-aspirin", *MORE_WARMING],
            "acceptablePathways": base.build()["extensions"]["tcmcraft"]["acceptablePathways"] + [
                {"id": "damp-heat-revision", "decisionPoint": "review", "interventions": ["rx-v3-damp-heat", "dispense-v3"],
                 "rationale": "A heat-clearing, damp-draining version 3 (Si Miao Wan type); other expert-endorsed damp-heat formulas would be equally acceptable."},
            ],
            "expertDisagreement": base.build()["extensions"]["tcmcraft"]["expertDisagreement"] + [
                "Whether to keep tonifying the underlying liver–kidney insufficiency alongside clearing damp-heat, or to clear first and tonify later (the case clears first).",
            ],
            "followUpModel": "authored branch: the pattern transforms with treatment, diet and season (not a calibrated outcome model)",
        },
    )
