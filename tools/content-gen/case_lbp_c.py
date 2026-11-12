"""Case tcm-sg-lbp-03 — family sg-lbp, review C: an execution discrepancy found at the one-week review.

The first visit is tcm-sg-lbp-01's, unchanged. At the review he has improved less than expected although he did
everything he was told in writing: the dispensary's label read "1 sachet once daily", while prescription version 2
(and the verbal counselling) said twice daily. He followed the printed label and received half the intended dose.
It is neither non-adherence nor a wrong pattern. The learner compares the prescription, the dispensing record and
label, and what he actually took; reports the discrepancy without blame; has the label corrected; explains and
apologises; and continues at the prescribed dose.

Phase 2 dimension: an execution discrepancy (DESIGN §3 contribution 4, §5.2 "a discrepancy between the current
prescription and the supplied medicines").
"""

from __future__ import annotations

import case_lbp as base
import lbp_family
from case_lbp import AUTHORED, FOLLOWUP, KW, L, U, answer, ask, ex, examine, hx, intervene, iv, opt, order_read
from common import dates

CASE_ID = "tcm-sg-lbp-03"

HISTORY = [
    hx("h-fu-status", "hpi",
       L("这一个星期腰怎么样了？", "How has your back been this past week?"),
       L("好一点点，现在大概五分，早上僵的时间短了一些。可是你说的我全部都照做了，我以为会好得多。",
         "A little better — about a five now, and the morning stiffness is a bit shorter. But I did everything you said, so I thought it would be much better than this."),
       KW(["这个星期", "这一周", "这周", "好点了吗", "好一点", "有没有好转", "上次以后"],
          ["this week", "past week", "improved", "any better", "progress", "since last time"]),
       required=True, phases=FOLLOWUP, supersedes=["h-presenting", "h-severity", "h-character"]),
    hx("h-fu-how-taken", "medications",
       L("你每天具体吃几包？药袋上的标签是怎么写的？", "Exactly how many sachets a day did you take, and what does the label on the bag say?"),
       L("一天一包。标签上写“每次1包，每日1次”。你那天好像有说晚上也要吃，可是我想还是照印出来的吃比较准。",
         "One a day. The label says \"1 sachet once daily\". I think you said something about the evening too, but I thought what's printed must be right, so I followed that."),
       KW(["一天吃几包", "每天几次", "一天几次", "标签", "药袋上", "怎么写的"], ["sachets a day", "times a day", "label", "per day", "the bag says"]),
       required=True, phases=FOLLOWUP),
    hx("h-fu-adherence", "medications",
       L("颗粒冲剂有没有按时吃？", "Have you been taking the granules as we agreed?"),
       L("有，每天早上早餐后一包，一次都没漏，完全照标签吃。", "Yes — one sachet every morning after breakfast, never missed one, exactly as the label says."),
       KW(["按时吃", "有没有吃药", "颗粒", "冲剂", "漏吃", "忘了吃", "中药吃了吗"],
          ["granules", "sachets", "taking the herbs", "missed doses", "missed any", "adherence", "remember to take"]),
       required=True, phases=FOLLOWUP),
    hx("h-fu-exercise", "functional",
       L("运动和坐姿方面的建议有做到吗？", "How did you get on with the exercises and the advice about sitting?"),
       L("伸展早晚都有做，在控制室每隔四十多分钟就起来走一下，也带了外套。", "I did the stretches morning and evening, got up every forty-odd minutes in the control room, and took a jacket."),
       KW(["伸展", "运动做了吗", "练习", "坐姿", "起来活动", "外套"], ["exercises", "stretches", "stretching", "sitting breaks", "the advice", "jacket"]),
       phases=FOLLOWUP),
    hx("h-fu-adverse", "other",
       L("治疗以后有没有什么不舒服或者副作用？", "Any side effects or problems since the treatment?"),
       L("没有。胃没有不舒服，没有瘀青或出血，大便颜色正常。",
         "Nothing. No stomach upset, no bruising or bleeding, and my stools are a normal colour."),
       KW(["副作用", "不良反应", "治疗以后", "胃不舒服", "头晕", "针以后"], ["side effects", "sideeffects", "problems since", "upset stomach", "giddy"]),
       phases=FOLLOWUP, supersedes=["h-bruising"]),
    hx("h-fu-redflags", "ros",
       L("现在腿脚有没有麻木无力？大小便正常吗？", "Any numbness or weakness in your legs now, and are your bladder and bowels normal?"),
       L("都没有，腿不麻，也有力气，大小便都正常。", "None of that — my legs are fine, no numbness, and everything's normal down below."),
       KW(["现在腿", "现在大小便", "现在有没有麻", "新的麻木"], ["new weakness", "new numbness", "newnumbness", "still no numbness"]),
       required=True, phases=FOLLOWUP, supersedes=["h-redflag-neuro", "h-redflag-ce"]),
    hx("h-fu-other-care", "medications",
       L("这一周有没有看别的医生，或者开始吃新的药？", "Have you seen any other doctor or started anything new this week?"),
       L("没有。照样吃我那三粒药，阿司匹林也每天吃。", "No. Same three pills as always, the aspirin included, every day."),
       KW(["别的医生", "看过医生", "新的药", "其他治疗", "别的药"], ["other doctor", "newmedicine", "startedanything", "other treatment", "seen anyone"]),
       phases=FOLLOWUP),
]

EXAM = [
    ex("e-fu-lumbar", "musculoskeletal",
       L("复查腰部压痛与活动度", "Re-examine lumbar tenderness and range of movement"),
       L("椎旁压痛略减，仍以右侧L4–S1为主；前屈指尖达小腿下段；后伸轻度痛；腰部皮温仍偏凉。",
         "Paravertebral tenderness slightly less, still mainly right L4–S1; flexion to fingertips at the lower shin; extension mildly painful; the lower back still cool to touch."),
       KW(["复查腰部", "腰部压痛", "活动度", "弯腰", "触诊腰部"], ["re-examine the back", "tenderness", "range of movement", "bend forward", "palpate"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-sites", "skin",
       L("查看腰背部与腘窝皮肤（上次如有针刺，含针刺部位）", "Inspect the skin of the back and behind the knees (last week's needling sites, if he was needled)"),
       L("皮肤完整，无瘀斑、红肿、硬结或感染迹象。", "Skin intact: no bruising, redness, swelling, lump or sign of infection."),
       KW(["针刺部位", "针眼", "瘀斑", "膝盖后面", "皮肤"], ["needling sites", "needle sites", "bruise", "behind the knee", "skin"]),
       phases=FOLLOWUP),
    ex("e-fu-neuro", "neurological",
       L("复查双下肢神经系统与直腿抬高", "Repeat the lower-limb neurological check and straight-leg raise"),
       L("肌力、反射与轻触觉均正常，与上周一致；直腿抬高双侧80°，无下肢痛。",
         "Power, reflexes and light touch normal and unchanged from last week; straight-leg raise 80° on both sides without leg pain."),
       KW(["神经系统", "肌力", "反射", "直腿抬高", "感觉"], ["neuro", "neurological", "power", "reflexes", "straight leg raise"]),
       required=True, phases=FOLLOWUP, requires=["reflex-hammer"]),
    ex("e-fu-tongue", "heent",
       L("复查舌象（漱口后、自然光下）", "Re-inspect the tongue (rinsed, in daylight)"),
       L("舌淡，稍胖大，边有齿痕；苔薄白腻，与上周相仿。", "Pale, slightly enlarged with tooth marks; coating thin, white and greasy, much as last week."),
       KW(["舌", "舌象", "舌苔", "望舌"], ["tongue", "coating", "inspect the tongue"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-pulse", "cardiovascular",
       L("复诊切脉", "Retake the pulse"),
       L("脉沉细，尺脉弱；72次/分，节律齐。", "Deep and thready, chi positions weak; 72/min, regular."),
       KW(["切脉", "把脉", "脉象", "号脉"], ["pulse", "radial pulse", "take the pulse"]),
       abnormal=True, phases=FOLLOWUP),
]

INVESTIGATIONS = [
    # replaces the base's review-time text of the same record: the first visit's dispensing, as it was actually done
    {
        "id": "dispensing-record",
        "name": L("调剂与发药记录", "Dispensing record"),
        "category": "record",
        "aliases": KW(["发药记录", "调剂记录", "配药记录"], ["dispensing record", "supply record", "what was dispensed"]),
        "requires": ["records"],
        "risk": "none",
        "performedAt": "records",
        "value": "essential",
        "availability": {"historical": False},
        "results": {
            "followup": {
                "date": L("上周初诊当日", "Last week, on the day of the first visit"),
                "text": L(
                    "按处方医师签署的第2版处方调剂（第1版作废，未调剂）：配方颗粒14包。\n"
                    "第2版处方用法：每次1包，每日2次，饭后温水冲服，共7天。\n"
                    "实际打印的标签：“陈伟良 — 独活寄生汤加减配方颗粒 — 每次1包，每日1次，饭后温水冲服 — 共14包”。\n"
                    "发药时已作用药交代（记录为“按标签说明”）。用药记录已更新：加入阿司匹林100 mg 每日一次。",
                    "Filled from prescription version 2 as signed by the prescriber (version 1 cancelled, never filled): 14 sachets of concentrated granules.\n"
                    "Directions on prescription version 2: 1 sachet twice daily after meals in warm water, for 7 days.\n"
                    "Label as printed: \"Tan Wee Liang — modified Du Huo Ji Sheng Tang granules — 1 sachet once daily after meals in warm water — 14 sachets\".\n"
                    "Counselling at supply recorded as \"as per label\". Medication record updated: aspirin 100 mg once daily added.",
                ),
                "source": AUTHORED,
            }
        },
    },
    {
        "id": "medicine-bag",
        "name": L("查看患者带来的药袋与标签", "Look at the medicine bag and label he brought"),
        "category": "bedside",
        "aliases": KW(["药袋", "药包标签", "看标签", "标签"], ["medicine bag", "the label", "look at the label", "bag label"]),
        "risk": "none",
        "performedAt": "bedside",
        "value": "essential",
        "results": {
            "followup": {
                "date": L("今日复诊", "Today's review"),
                "text": L("药袋标签：“每次1包，每日1次，饭后温水冲服 — 共14包”。袋内剩余7包。",
                          "The bag's label reads: \"1 sachet once daily after meals in warm water — 14 sachets\". Seven sachets are left in the bag."),
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
        "value": "useful",
        "results": {
            "followup": {
                "date": L("今日复诊", "Today's review"),
                "text": L("与患者一起清点：14包中剩余7包（服用7包）。服药记录：7天每天早上一包，没有漏服。",
                          "Counted with him: 7 of 14 sachets left (7 taken). Dose diary: one sachet every morning for 7 days, none missed."),
                "note": L("与标签一致，与处方不一致。", "Consistent with the label, not with the prescription."),
                "source": AUTHORED,
            }
        },
    },
]

COMPARED = {"all": [{"read": "dispensing-record"}, {"any": [{"read": "medicine-bag"}, {"read": "sachet-count"}]}]}

BASE_CONTINUE = next(i for i in base.INTERVENTIONS if i["id"] == "continue-course")

INTERVENTIONS = [
    iv("incident-report", "other",
       L("把标签与处方不符作为调剂差错（无责报告）上报，并与药房一起回顾", "Report the label–prescription mismatch as a dispensing incident (no-blame) and review it with the dispensary"),
       KW(["上报", "差错报告", "不良事件报告", "事件上报"], ["incident report", "report the error", "dispensing incident", "no-blame report"]),
       risk="none", checklist=True, setFlags=["incident-reported"],
       contraindicatedWhen={"not": COMPARED},
       harm=L("还没有把处方、调剂记录与标签或实际服药情况对照过，无从判断是否有差错。",
              "You have not yet compared the prescription with the dispensing record and the label or what he took, so there is no discrepancy on record to report."),
       response=L("药房林先生确认标签模板默认为“每日1次”，第2版处方的用法没有同步过去；已登记为调剂差错，并改为发药前由第二人核对标签。",
                  "Mr Lim at the dispensary finds that the label template defaulted to \"once daily\" and version 2's directions were not carried over; it is logged as a dispensing incident, and a second-person label check before supply is introduced.")),
    iv("relabel-explain", "medication",
       L("请药房按第2版更正标签，并向他说明差错与正确用法、表示歉意", "Have the dispensary correct the label to match version 2, and explain the error and the right dose to him with an apology"),
       KW(["更正标签", "重新贴标签", "改标签", "道歉", "说明差错"], ["correct the label", "relabel", "apologise", "explain the error", "open disclosure"]),
       risk="none", checklist=True, setFlags=["label-corrected"],
       contraindicatedWhen={"not": COMPARED},
       harm=L("还没有核对标签与处方，不能确定要更正什么。", "You have not checked the label against the prescription yet, so it is not clear what needs correcting."),
       response=L("新标签写明“每次1包，每日2次”。他松了一口气：“原来不是我吃错了。”", "The new label reads \"1 sachet twice daily\". He looks relieved: \"So it wasn't me getting it wrong.\"")),
    BASE_CONTINUE,
    iv("adherence-counsel", "other",
       L("提醒他要记得吃晚上那包", "Counsel him to remember his evening dose"),
       KW(["提醒晚上吃", "记得吃药", "依从性教育", "别忘了"], ["remember the evening dose", "adherence counselling", "don't forget", "reminders"]),
       risk="none",
       response=L("他一脸疑惑：“可是标签上写一天一次啊……”", "He looks puzzled: \"But the label says once a day…\"")),
    iv("switch-damp-heat", "medication",
       L("改用清热利湿方（四妙丸类）", "Switch to a heat-clearing, damp-draining formula (四妙丸 type)"),
       KW(["四妙丸", "清热利湿", "改方", "湿热方"], ["si miao", "clear heat", "damp-heat formula", "switch formula"]),
       scope="medical", risk="low",
       contraindicatedWhen={"always": True},
       harm=L("与证不符：他仍畏寒、舌淡苔白、脉沉细，是寒湿而非湿热，苦寒之品会伤阳。疗效有限是因为标签差错让他只服了一半剂量，不是辨证错误。",
              "It does not fit the pattern: he still feels the cold, with a pale tongue, a white coating and a deep, thready pulse — cold-damp, not damp-heat — and bitter-cold herbs injure yang. The limited response comes from a labelling error that halved his dose, not from a wrong pattern."),
       response=L("新处方已开出。", "The new prescription is written.")),
    iv("double-dose", "medication",
       L("每天早上一次吃两包补回剂量", "Have him take two sachets at once each morning to make up"),
       KW(["加倍", "一次两包", "补服", "双倍"], ["double the dose", "two at once", "make up doses", "twiceasmuch"]),
       scope="medical", risk="moderate",
       contraindicatedWhen={"always": True},
       harm=L("一次两包不等于每日两次：单次剂量超过处方，也解决不了标签的问题。应更正标签，按处方每日两次服用。",
              "Two sachets at once is not twice daily: it doubles the single dose beyond the prescription and leaves the label wrong. Correct the label and resume the prescribed twice-daily schedule."),
       response=L("用法已改。", "The instructions are changed.")),
]

DECISIONS = [
    {
        "id": "d-followup", "kind": "single",
        "prompt": L("他完全按照药袋标签服药，但改善不如预期。最能解释这一结果的是什么？下一步怎么做？",
                    "He took the granules exactly as the label on the bag says, yet he has improved less than expected. What best explains this, and what next?"),
        "requires": {"all": [{"asked": "h-fu-how-taken"}, {"asked": "h-fu-redflags"}, {"examined": "e-fu-neuro"}, COMPARED]},
        "need": L("先问清楚他具体怎么服药、复查危险信号与神经系统，并把调剂记录与药袋标签或剩余药包对照。",
                  "First establish exactly how he took the medicine, re-check the danger signs and nerves, and compare the dispensing record with the bag's label or the sachets left."),
        "options": [
            opt("label-error", True,
                L("执行差错：标签（每日1次）与第2版处方（每日2次）不符，他只服了一半剂量——按无责原则上报调剂差错，更正标签并向他说明、致歉，按处方剂量继续，维持原评估",
                  "An execution discrepancy: the label (once daily) does not match prescription version 2 (twice daily), so he has had half the intended dose — report it as a no-blame dispensing incident, have the label corrected, explain and apologise to him, continue at the prescribed dose and keep the assessment"),
                L("正确。处方、调剂记录与标签、实际服药三者对照，差错出在标签，不在患者，也不在辨证。上报是为了修正系统（发药前第二人核对），向患者说明与致歉是开放披露。",
                  "Correct. Comparing the prescription, the dispensing record and label, and what he actually took puts the error in the label — not in the patient and not in the pattern. Reporting fixes the system (a second check of labels before supply); explaining and apologising to him is open disclosure.")),
            opt("adherence", False,
                L("他忘了吃晚上那包：做依从性教育", "He forgot the evening doses: counsel him on adherence"),
                L("不对。他完全照标签做了，记录显示标签是错的。把系统差错归咎于患者既不准确，也会损害信任，而且下周还会照错的标签吃。",
                  "No. He did exactly what the label told him, and the record shows the label was wrong. Blaming him for a system error is inaccurate, damages trust, and leaves him following the wrong label next week.")),
            opt("wrong-pattern", False,
                L("证候判断错误，应改方", "The pattern was wrong: switch the formula"),
                L("不对。舌脉与症状和初诊一致，他只服了一半剂量，不能据此判断方证不符。",
                  "No. His symptoms, tongue and pulse match the first visit, and he has taken half the dose; that cannot show the formula was wrong for the pattern.")),
            opt("double", False,
                L("每天早上一次吃两包补回来", "Give two sachets at once each morning to catch up"),
                L("不对。单次加倍不等于每日两次，也没有更正错误的标签。",
                  "No. Doubling a single dose is not the same as twice daily, and it leaves the wrong label in place.")),
            opt("stop", False,
                L("中药没效，停掉中药只做针灸", "The herbs are not working: stop them and rely on acupuncture"),
                L("不对。他还没有真正按处方剂量服过药，无从判断中药是否有效。",
                  "No. He has not yet taken the herbs at the prescribed dose, so whether they work is unknown.")),
        ],
    }
]

OBJECTIVES = [
    {"id": "o-followup", "title": L("一周复诊：核对执行情况并修订方案", "One-week review: check what was actually done and revise the plan"),
     "short": L("复诊", "Review"),
     "hint": L("先弄清楚他实际接受了哪些治疗、实际服了多少药、是怎么服的，再把处方、调剂记录和他手上的药对照起来判断。",
               "First establish what treatment he actually received and how much medicine he took, and how; then compare the prescription, the dispensing record and the medicine in his hands before you judge."),
     "guidance": L("在诊室与陈先生复诊。", "Review Mr Tan in the consulting room."),
     "completeWhen": {"all": [{"decided": "d-followup"}, {"intervened": "relabel-explain", "valid": True}, {"intervened": "incident-report", "valid": True}, {"intervened": "continue-course"}]},
     "waypoints": [{"unless": {"read": "dispensing-record"}, "target": "records"}, {"target": "patient"}]},
]

RUBRIC = [
    {"id": "r-execution-check", "domain": "investigations", "weight": 3,
     "text": L("复诊时把处方、调剂记录与标签和实际服药情况对照", "At review, compared the prescription, the dispensing record and label, and what he actually took"),
     "met": {"all": [{"asked": "h-fu-how-taken"}, COMPARED]}},
    {"id": "r-followup", "domain": "management", "weight": 3,
     "text": L("首次即把有限的疗效归因于执行差错，且没有改方或加倍剂量", "Attributed the limited response to the execution discrepancy first time, without changing the formula or doubling the dose"),
     "met": {"all": [{"decidedFirstTry": "d-followup"}, {"not": {"intervened": "switch-damp-heat"}}, {"not": {"intervened": "double-dose"}}]},
     "scoredWhen": {"any": [{"phase": "followup"}, {"intervened": "switch-damp-heat"}, {"intervened": "double-dose"}]}},
    {"id": "r-relabel", "domain": "safety", "weight": 3, "critical": True,
     "text": L("更正标签，使发出的药与现行处方一致", "Had the label corrected so the supplied medicine matches the current prescription"),
     "met": {"intervened": "relabel-explain", "valid": True}},
    {"id": "r-incident", "domain": "safety", "weight": 2,
     "text": L("按无责原则上报调剂差错", "Reported the dispensing incident without blame"),
     "met": {"intervened": "incident-report", "valid": True}},
    {"id": "r-no-blame", "domain": "management", "weight": 1,
     "text": L("没有把系统差错当作患者依从性问题来处理", "Did not treat the system error as the patient's non-adherence"),
     "met": {"not": {"intervened": "adherence-counsel"}},
     "scoredWhen": {"any": [{"phase": "followup"}, {"intervened": "adherence-counsel"}]}},
    {"id": "r-comm-disclosure", "domain": "communication", "weight": 1,
     "text": L("向他坦诚说明差错并致歉（开放披露）", "Told him openly about the error and apologised (open disclosure)"),
     "judgeGuidance": L("学员是否用通俗语言说明标签印错、他照做并没有错、这对疗效的影响、接下来如何改正（新标签、每日两次）以及诊所为防止再发做了什么，并真诚致歉？",
                        "Did the learner explain in plain words that the label was printed wrongly, that he did nothing wrong in following it, how it affected his progress, how it will be put right (a new label, twice daily) and what the clinic is doing to stop it happening again — with a sincere apology?")},
]

SAFETY_GATES = [
    {"id": "g-label-left-wrong", "verdict": "complication",
     "label": L("继续疗程但没有更正错误的标签", "Course continued with the wrong label left in place"),
     "when": {"all": [{"intervened": "continue-course"}, {"not": {"intervened": "relabel-explain", "valid": True}}]}},
]

SOLUTION = [
    *ask("h-fu-status", "h-fu-how-taken", "h-fu-adherence", "h-fu-exercise", "h-fu-adverse", "h-fu-redflags", "h-fu-other-care"),
    *examine("e-fu-lumbar", "e-fu-sites", "e-fu-neuro", "e-fu-tongue", "e-fu-pulse"),
    *order_read("dispensing-record", "followup"),
    *order_read("medicine-bag", "followup"),
    *order_read("sachet-count", "followup"),
    *order_read("acupuncture-record", "followup"),
    answer("d-followup", "label-error"),
    *intervene("incident-report", "relabel-explain", "continue-course"),
    {"type": "finish"},
]

UTTERANCES = [
    U("这个星期有没有好一点？", "zh-CN", "h-fu-status"),
    U("is it any better than last week?", "en", "h-fu-status"),
    U("一天吃几包？", "zh-CN", "h-fu-how-taken"),
    U("what does the label say?", "en", "h-fu-how-taken"),
    U("颗粒有没有漏吃？", "zh-CN", "h-fu-adherence"),
    U("have you missed any doses?", "en", "h-fu-adherence"),
    U("现在大小便正常吗，腿有没有无力？", "zh-CN", "h-fu-redflags"),
    U("any new weakness or numbness in the legs?", "en", "h-fu-redflags"),
    U("伸展有没有每天做？", "zh-CN", "h-fu-exercise"),
]

OUTCOME = L("复诊时把处方、调剂记录与标签和实际服药情况对照，识别标签差错这一系统问题，按无责原则上报、更正并向患者开放披露，同时不改变站得住脚的评估。",
            "At review, compare the prescription, the dispensing record and label, and what the patient actually took; recognise a labelling error as a system problem, report it without blame, correct it and disclose it to the patient, without changing a sound assessment.")

DEBRIEF = {
    "title": L("复盘：复发性腰痛——执行差错", "Debrief: recurrent low back pain — an execution discrepancy"),
    "conclusion": L(
        "初诊同 tcm-sg-lbp-01。复诊时他完全照药袋标签服药，却改善有限：标签印的是“每日1次”，第2版处方是每日2次，他只服了一半剂量。这既不是依从性问题，也不是辨证错误，而是执行差错。正确做法是按无责原则上报、更正标签、向他说明并致歉，按处方剂量继续疗程并再评估。",
        "First visit as in tcm-sg-lbp-01. At the review he had followed the bag's label exactly, yet improved only a little: the label said once daily while prescription version 2 said twice daily, so he took half the intended dose. This is neither non-adherence nor a wrong pattern but an execution discrepancy. The right course is to report it without blame, correct the label, explain and apologise to him, and continue at the prescribed dose with a further review.",
    ),
    "keyReasoning": base.DEBRIEF["keyReasoning"][:4] + [
        L("在把有限的疗效归因于患者或证候之前，先对照“开了什么、发了什么、标签写了什么、实际吃了什么”：差错可能在系统里。",
          "Before blaming a limited response on the patient or the pattern, compare what was prescribed, what was supplied and labelled, and what was actually taken: the gap may be in the system."),
    ],
    "teachingPoints": base.DEBRIEF["teachingPoints"] + [
        L("执行差错（标签与处方不符）要通过对照处方版本、调剂记录、标签与患者实际做法来发现；按无责原则上报，向患者开放披露并致歉（参见世卫组织“用药无伤害”全球患者安全挑战，2017）。",
          "Execution discrepancies (a label that differs from the prescription) are found by comparing the prescription version, the dispensing record, the label and what the patient did; they are reported without blame and disclosed to the patient with an apology (see WHO Medication Without Harm, 2017)."),
    ],
    "references": base.REFERENCES + [
        "World Health Organization. Medication without harm: WHO global patient safety challenge on medication safety. Geneva: WHO; 2017.",
    ],
}


def build() -> dict:
    c = lbp_family.variant(
        case_id=CASE_ID,
        version="0.2.0",
        variant_id="review-c-execution-discrepancy",
        title=L("腰痛反复发作 · 52岁男性 · 复诊C", "Recurrent low back pain · 52-year-old man · review C"),
        outcome=OUTCOME,
        review={"history": HISTORY, "exam": EXAM, "investigations": INVESTIGATIONS, "interventions": INTERVENTIONS, "decisions": DECISIONS,
                "objectives": OBJECTIVES, "rubric": RUBRIC, "safetyGates": SAFETY_GATES, "solution": SOLUTION, "utterances": UTTERANCES},
        debrief=DEBRIEF,
        tcmcraft={
            "dates": dates("2026-11-07"),
            "unacceptable": ["rx-verbal-swap", "stop-aspirin", "switch-damp-heat", "double-dose"],
            "followUpModel": "authored branch: a dispensing label that differs from the prescription (not a calibrated outcome model)",
        },
    )
    return c
