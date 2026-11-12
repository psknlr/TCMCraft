"""Case tcm-sg-lbp-02 — family sg-lbp, review B: new neurological danger signs at the one-week review.

The first visit is tcm-sg-lbp-01's, unchanged (lbp_family.first_visit). Two days before the review he lifted a carton
at work. Since then he has had bilateral sciatica (left worse), numbness in the saddle area and, since this morning,
hesitancy with a thin urinary stream, without retention or incontinence: suspected cauda equina syndrome. The review
is no longer about the TCM pattern. The right course is to stop TCM treatment and transfer him at once to an
Emergency Department for same-day assessment and emergency MRI, with a written handover.

Phase 2 dimension: an alternative follow-up branch that requires a care transition (DESIGN §7, escalation variant).
"""

from __future__ import annotations

import case_lbp as base
import lbp_family
from case_lbp import FOLLOWUP, KW, L, U, answer, ask, ex, examine, hx, intervene, iv, opt
from common import dates

CASE_ID = "tcm-sg-lbp-02"

DANGER_EVIDENCE = {"any": [{"asked": "h-fu-redflags"}, {"asked": "h-fu-status"}, {"examined": "e-fu-neuro"}]}

HISTORY = [
    hx("h-fu-status", "hpi",
       L("这一个星期腰怎么样了？", "How has your back been this past week?"),
       L("头几天好了一些。可是前天上班搬一箱货，腰里像有什么东西“啪”一下，之后痛就往两条腿下面窜，左边更厉害，一直到脚底。现在痛到八分。",
         "It was better for the first few days. But the day before yesterday I lifted a carton at work and felt something go in my back — since then the pain shoots down both legs, worse on the left, right down to the sole of my foot. It's an eight now."),
       KW(["这个星期", "这一周", "这周", "好点了吗", "有没有好转", "上次以后", "上周以后", "两条腿都痛", "痛到脚底", "往下窜"],
          ["this week", "past week", "any better", "progress", "since last time", "since last week", "both legs hurt", "downtothesole"]),
       required=True, phases=FOLLOWUP, supersedes=["h-presenting", "h-severity", "h-character"]),
    hx("h-fu-onset-time", "hpi",
       L("下面发麻和小便困难具体是什么时候开始的？", "When exactly did the numbness down below and the trouble passing urine start?"),
       L("下面发麻是昨天下午四点多发现的；小便难是今天早上开始的。", "I noticed the numbness yesterday at about four in the afternoon; the trouble passing water started this morning."),
       KW(["什么时候开始", "几点开始", "开始的时间", "什么时候发现", "具体时间"], ["exactly when", "what time", "since when", "when exactly"]),
       required=True, phases=FOLLOWUP),
    hx("h-fu-redflags", "ros",
       L("现在腿脚有没有麻木无力？大小便正常吗？", "Any numbness or weakness in your legs now, and are your bladder and bowels normal?"),
       L("两只脚都麻，左脚有点没力，走路会拖。昨天开始，上完厕所擦的时候下面麻麻的，像隔着一层棉花。今天早上小便要用力才出得来，尿得很细。没有尿裤子。",
         "Both feet are numb, and my left foot is weak — it drags when I walk. Since yesterday, when I wipe after the toilet it feels numb down there, like through cotton wool. This morning I had to strain to pass water, and the stream was thin. I haven't wet myself."),
       KW(["现在腿", "现在大小便", "现在有没有麻", "新的麻木", "小便解得出", "解得出来", "尿得出", "尿不出", "使劲", "用力才",
           "排尿困难", "小便困难", "小便问题", "小便没有问题", "小便没问题", "尿得细", "会阴", "下面麻", "擦屁股", "纸碰到"],
          ["new weakness", "new numbness", "newnumbness", "anything new in your legs", "pass urine", "passing urine", "strain to pass",
           "trouble peeing", "saddle", "wiping", "down below"]),
       required=True, phases=FOLLOWUP, supersedes=["h-redflag-neuro", "h-redflag-ce"],
       safety={"datum": "cauda-equina-review", "finding": "positive"}),
    hx("h-fu-bowel", "ros",
       L("上一次大便是什么时候？有没有控制不住或者没感觉？", "When did you last open your bowels, and can you feel and control them normally?"),
       L("昨天早上大过一次，之后就没有了。没有控制不住。", "Yesterday morning, not since. No accidents."),
       KW(["上一次大便", "排便", "大便最后", "大便有没有"], ["open your bowels", "last bowel", "bowels opened"]),
       phases=FOLLOWUP),
    hx("h-fu-meds-last", "medications",
       L("这两天吃了哪些药？阿司匹林最后一次是什么时候吃的？", "What medicines have you taken in the last two days, and when was your last aspirin?"),
       L("阿司匹林今天早上七点吃了，颗粒今天早上也吃了。昨晚痛得受不了，在药房买了布洛芬，吃了两粒，一粒200毫克。",
         "Aspirin at seven this morning, and the granules this morning too. Last night the pain was too much, so I bought ibuprofen at the pharmacy and took two — 200 milligrams each."),
       KW(["最后一次吃", "上一次吃药", "这两天吃了", "止痛药", "布洛芬"], ["last dose", "last took", "painkillers", "ibuprofen", "taken since"]),
       required=True, phases=FOLLOWUP, supersedes=["h-meds", "h-antithrombotic"]),
    hx("h-fu-adherence", "medications",
       L("颗粒冲剂有没有按时吃？", "Have you been taking the granules as we agreed?"),
       L("早晚各一包，每天都有吃，前天开始痛得厉害也还是照吃。", "One in the morning and one in the evening, every day — even since the pain got bad."),
       KW(["按时吃", "颗粒", "冲剂", "漏吃", "吃了几包"], ["granules", "sachets", "missed doses", "taking the herbs"]),
       phases=FOLLOWUP),
    hx("h-fu-adverse", "other",
       L("治疗以后有没有什么不舒服或者副作用？", "Any side effects or problems since the treatment?"),
       L("胃没有不舒服，没有瘀青或出血。", "No stomach upset, no bruising or bleeding."),
       KW(["副作用", "不良反应", "治疗以后", "胃不舒服"], ["side effects", "sideeffects", "problems since", "upset stomach"]),
       phases=FOLLOWUP, supersedes=["h-bruising"]),
]

EXAM = [
    ex("e-fu-general", "general",
       L("观察神色、坐姿与步态", "Observe his distress, how he sits and how he walks"),
       L("表情痛苦，坐时身体向右侧倾；行走缓慢跛行，左足落地时轻度拍地。", "In obvious pain, sitting tilted to the right; walks slowly with a limp, the left foot slapping slightly as it lands."),
       KW(["望诊", "步态", "坐姿", "一般情况"], ["general appearance", "gait", "walking", "inspection"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-neuro", "neurological",
       L("复查双下肢神经系统（肌力、反射、感觉，包括鞍区）", "Repeat the lower-limb neurological examination (power, reflexes, sensation including the saddle area)"),
       L("左踝背屈、拇背伸肌力4级，右侧5级；左踝反射消失，右踝反射减弱，双膝反射存在。左足外侧及双足底轻触觉减退；患者诉肛周及会阴发麻，双侧臀内侧轻触觉较大腿减退。肛门指检与膀胱残余尿评估需在急诊进行。",
         "Left ankle dorsiflexion and great-toe extension 4/5, right 5/5; left ankle reflex absent, right reduced, knee reflexes present. Light touch reduced over the outer left foot and both soles; he reports numbness around the back passage and between the legs, and light touch over both inner buttocks is reduced compared with the thighs. A rectal examination and a bladder residual-volume check are for the Emergency Department."),
       KW(["神经系统", "肌力", "反射", "感觉检查", "鞍区", "腱反射"], ["neuro", "neurological", "power", "reflexes", "sensation", "saddle"]),
       abnormal=True, required=True, phases=FOLLOWUP, requires=["reflex-hammer"]),
    ex("e-fu-slr", "neurological",
       L("复查直腿抬高试验", "Repeat the straight-leg raise"),
       L("直腿抬高左侧35°、右侧50°，均诱发膝以下放射痛。", "Straight-leg raise 35° on the left and 50° on the right, both reproducing pain below the knee."),
       KW(["直腿抬高", "抬腿试验"], ["straight leg raise", "straightlegraise", "slr"]),
       abnormal=True, required=True, phases=FOLLOWUP),
    ex("e-fu-abdomen", "abdomen",
       L("检查下腹部（膀胱区）", "Examine the lower abdomen (bladder)"),
       L("下腹软，耻骨上未见明显膨隆、无压痛。本诊所没有膀胱扫描仪，无法测量膀胱容量。",
         "Lower abdomen soft; no obvious suprapubic swelling or tenderness. This clinic has no bladder scanner, so the bladder volume cannot be measured here."),
       KW(["下腹", "膀胱区", "耻骨上", "腹部"], ["lower abdomen", "bladder", "suprapubic", "abdomen"]),
       phases=FOLLOWUP),
    ex("e-fu-lumbar", "musculoskeletal",
       L("复查腰部", "Re-examine the lower back"),
       L("腰部广泛压痛，椎旁肌痉挛；因疼痛无法完成活动度检查。", "Diffuse lumbar tenderness with paraspinal spasm; movement too painful to test."),
       KW(["腰部", "压痛", "活动度", "触诊腰部"], ["lower back", "tenderness", "range of movement", "palpate"]),
       abnormal=True, phases=FOLLOWUP),
    ex("e-fu-tongue", "heent",
       L("复查舌象（漱口后、自然光下）", "Re-inspect the tongue (rinsed, in daylight)"),
       L("舌淡，边有齿痕；苔薄白腻。", "Pale with tooth marks; coating thin, white and greasy."),
       KW(["舌", "舌象", "舌苔", "望舌"], ["tongue", "coating", "inspect the tongue"]),
       phases=FOLLOWUP),
    ex("e-fu-pulse", "cardiovascular",
       L("复诊切脉", "Retake the pulse"),
       L("脉弦数，96次/分，节律齐。", "Wiry and rapid, 96/min, regular."),
       KW(["切脉", "把脉", "脉象", "号脉"], ["pulse", "radial pulse", "take the pulse"]),
       abnormal=True, phases=FOLLOWUP),
]

TRANSFER_HARM = L(
    "目前没有需要急诊处理的表现：没有危险信号或神经根受累体征。只有出现马尾综合征征象、进行性无力、发热或明显外伤等情况，才需要紧急转诊。",
    "Nothing in his presentation needs emergency care now: there are no danger signs or signs of nerve-root involvement. Urgent referral is for signs such as cauda equina symptoms, progressive weakness, fever or significant trauma.",
)

DELAYS = ["acu-review-session", "continue-course", "wait-and-see", "herbs-stasis"]
# Treating or waiting instead of transferring. Every one of these is a checklist step that is refused at the review
# (not given, so on the static clock no time is lost) — tuina included. The engine cannot tell when a refused attempt
# was made, so a tuina refused at the first visit (before its prerequisites) also counts here.
REFUSED_DELAYS = [{"intervened": x} for x in DELAYS] + [{"intervened": "tuina", "valid": False}]
# The written handover can only state what has been established: the new symptoms and when each began, the
# neurological findings and the last doses.
HANDOVER_FACTS = {"all": [{"phase": "followup"}, {"asked": "h-fu-status"}, {"asked": "h-fu-redflags"}, {"asked": "h-fu-onset-time"},
                          {"asked": "h-fu-meds-last"}, {"examined": "e-fu-neuro"}]}

INTERVENTIONS = [
    # replaces the base's first-visit referral: the same act, appropriate only once new danger signs are known
    iv("refer-ed", "disposition",
       L("立即转往急诊", "Refer to the Emergency Department now"),
       KW(["急诊", "转急诊", "送医院", "紧急转诊", "叫救护车", "995"], ["emergency department", "aande", "urgent referral", "send to hospital", "ambulance", "995"]),
       dose=L("致电急诊说明情况；他走路困难、疼痛剧烈时由诊所拨打995叫救护车；不要让他自己开车。",
              "Phone the Emergency Department and tell them what you found; if he cannot walk safely or is in severe pain, the clinic calls 995 for an ambulance; he must not drive himself."),
       scope="medical", risk="none", checklist=True, setFlags=["ed-transfer"],
       contraindicatedWhen={"not": DANGER_EVIDENCE}, harm=TRANSFER_HARM,
       indicatedWhen={"asked": "h-fu-redflags"},
       response=L("急诊接诊医生同意接收，请诊所附上书面交接。因他行走困难、疼痛剧烈，诊所拨打995叫了救护车。",
                  "The Emergency Department doctor accepts him and asks for a written handover. Because he can barely walk and is in severe pain, the clinic calls 995 for an ambulance.")),
    iv("handover-initial", "consult",
       L("电话初步交接给急诊：只说目前已确认的，未核实的明确标为“未核实”，书面交接随后补上",
         "Initial handover to the Emergency Department by phone: only what is established so far, with anything not yet checked stated as unverified; the written handover follows"),
       KW(["电话交接", "初步交接", "先打电话交接"], ["initial handover", "phone handover", "handover by phone", "call the ed now"]),
       dose=L("说明：他是谁、为什么转诊（到目前为止他自己讲的新症状和你已查到的体征）、初诊已知的用药（阿司匹林100 mg 每日、氨氯地平、阿托伐他汀）与一周前开始的中药颗粒；明确哪些还没核实（各症状的起始时间、神经系统检查、最后一次服药时间），书面交接随后发出。",
              "Say who he is, why you are transferring him (the new symptoms as he has described them so far, and any signs you have found), his medicines as known from the first visit (aspirin 100 mg daily, amlodipine, atorvastatin) and the granules started a week ago; say plainly what is not yet checked (when each symptom began, the neurological examination, the time of each last dose), and that a written handover will follow."),
       scope="medical", risk="none", setFlags=["handover-initial"],
       contraindicatedWhen={"not": {"phase": "followup"}},
       harm=L("这一次就诊没有需要交接给急诊的内容。", "There is nothing to hand over to emergency care at this visit."),
       response=L("急诊护士记下初步交接，并标出待确认的项目。", "The Emergency Department nurse takes the initial handover and notes what is still to be confirmed.")),
    iv("handover-letter", "consult",
       L("书面交接给急诊：新症状及出现时间、检查所见、用药（含最后剂量）与中医治疗记录",
         "Written handover to the Emergency Department: new symptoms and when each began, examination findings, medicines with last doses, and the TCM treatment record"),
       KW(["交接", "交接单", "转诊信", "写给急诊"], ["handover", "referral letter", "letter to the ed", "written handover"]),
       dose=L("包括：前天搬重物后双下肢放射痛；昨天约16:00起鞍区麻木、今晨起排尿费力（无尿失禁）；左踝背屈4级、左踝反射消失、鞍区感觉减退；阿司匹林100 mg（今晨7:00）、布洛芬400 mg（昨晚）、氨氯地平、阿托伐他汀；中医治疗记录附后：一周来服独活寄生汤加减配方颗粒（已签发的第2版处方及其组成，今晨最后一次），以及针灸治疗记录（如有）。",
              "Include: radiating pain down both legs since lifting two days ago; saddle numbness since about 16:00 yesterday and straining to pass urine since this morning (no incontinence); left ankle dorsiflexion 4/5, absent left ankle reflex, reduced saddle sensation; aspirin 100 mg (07:00 today), ibuprofen 400 mg (last night), amlodipine, atorvastatin; the TCM treatment record attached: a week of modified Du Huo Ji Sheng Tang granules (the signed version 2 with its composition, last dose this morning) and the acupuncture session record, if a session was given."),
       requires=["records"], scope="medical", risk="none", checklist=True, setFlags=["handover-written"],
       contraindicatedWhen={"not": HANDOVER_FACTS},
       harm=L("书面交接只能写已经确认的内容：先问清楚这一周的变化、危险信号及各自的起始时间、最后一次服药，并复查神经系统。转诊不必等它——可以先电话初步交接，书面交接随后补上。",
              "The written handover can only state what has been established: first ask what changed this week, the danger signs and when each began, and the last doses, and repeat the neurological examination. The transfer need not wait for it — give an initial handover by phone now and send the letter when it is complete."),
       response=L("书面交接已发给急诊，并随他一起去医院；副本存档。", "The written handover is sent to the Emergency Department and goes with him; a copy is filed.")),
    iv("stop-tcm", "other",
       L("暂停中药颗粒和后续针灸，待急诊评估后再定", "Stop the herbal granules and further acupuncture until he has been assessed"),
       KW(["停中药", "暂停治疗", "停止针灸", "停颗粒"], ["stop the herbs", "pause treatment", "stop acupuncture", "hold the granules"]),
       scope="medical", risk="none", checklist=True, setFlags=["tcm-paused"],
       contraindicatedWhen={"not": {"phase": "followup"}},
       harm=L("还没有开始治疗，没有需要暂停的。", "Nothing has been started yet, so there is nothing to stop."),
       indicatedWhen={"asked": "h-fu-redflags"},
       response=L("他点头，把剩下的药包交给你保管。", "He nods and hands you the remaining sachets to keep.")),
    iv("acu-review-session", "procedure",
       L("今天针刺缓解腿痛", "Acupuncture today for the leg pain"),
       KW(["今天针灸", "再针一次", "针刺止痛", "扎针止痛"], ["acupuncture today", "needle again", "needling for pain", "second session"]),
       scope="medical", risk="moderate", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("新出现的双下肢放射痛、鞍区麻木和排尿困难提示疑似马尾综合征：针刺会拖延急诊评估与急诊MRI，而结局取决于在尿潴留出现之前及时减压。",
              "New pain down both legs, saddle numbness and difficulty passing urine point to suspected cauda equina syndrome: needling delays emergency assessment and MRI, and the outcome depends on decompression before urinary retention sets in."),
       response=L("针具已准备。", "The needles are ready.")),
    iv("continue-course", "disposition",
       L("继续既定针灸疗程与中药，两周后复诊", "Continue the planned acupuncture course and the herbs, and review in two weeks"),
       KW(["继续治疗", "继续疗程", "两周后复诊", "维持方案"], ["continue treatment", "continue the course", "carry on", "review in two weeks"]),
       risk="moderate", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("按原计划继续意味着把疑似马尾综合征留到两周后：今天就需要急诊评估和急诊MRI。",
              "Carrying on as planned leaves suspected cauda equina syndrome for two weeks: he needs emergency assessment and an emergency MRI today."),
       response=L("下次预约已排好。", "The next appointments are booked.")),
    iv("wait-and-see", "disposition",
       L("回家卧床休息，三天后复诊，如完全解不出小便再来", "Send him home to rest, review in three days, and come back if he cannot pass urine at all"),
       KW(["回家休息", "卧床休息", "三天后复诊", "观察几天"], ["rest at home", "bed rest", "review in three days", "wait and see"]),
       risk="high", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("等到完全尿潴留，就是在等结局更差的阶段。疑似马尾综合征不观察，今天就转急诊。",
              "Waiting for complete retention means waiting for the stage with the worse outcome. Suspected cauda equina syndrome is not watched: he goes to the Emergency Department today."),
       response=L("他慢慢走出诊室。", "He shuffles out of the room.")),
    iv("herbs-stasis", "medication",
       L("改用更强的活血化瘀方治疗刺痛", "Switch to a stronger blood-activating formula for the stabbing pain"),
       KW(["活血化瘀", "改方", "身痛逐瘀汤", "加强活血"], ["blood-activating formula", "switch formula", "stronger formula", "move the blood"]),
       scope="medical", risk="moderate", checklist=True,
       contraindicatedWhen={"always": True},
       harm=L("先处理危险信号：证候也许变了，但现在需要的是急诊评估。他同时服阿司匹林、昨晚又吃了布洛芬，可能还要手术，此时加强活血更增加出血风险。",
              "Danger signs come first: the pattern may well have changed, but what he needs now is emergency assessment. With aspirin, last night's ibuprofen and possible surgery ahead, stronger blood-activating herbs add bleeding risk."),
       response=L("新处方已写好。", "The new prescription is written.")),
    # replaces the base's version: at the review a routine referral is too slow
    iv("refer-imaging", "consult",
       L("转介做腰椎MRI", "Refer for a lumbar spine MRI"),
       KW(["核磁共振", "MRI", "腰椎MRI", "影像检查", "拍片"], ["mri", "lumbar mri", "imaging", "scan", "x-ray"]),
       risk="none",
       contraindicatedWhen={"phase": "followup"},
       harm=L("太慢了：疑似马尾综合征需要经急诊在数小时内完成急诊MRI，而不是常规预约。", "Too slow: suspected cauda equina syndrome needs an emergency MRI within hours through the Emergency Department, not a routine appointment."),
       response=L("常规的腰椎MRI转介信已写好，综合诊所会另行通知预约时间。", "A routine referral for a lumbar MRI is written; the polyclinic will send an appointment.")),
    # replaces the base's version: manual therapy waits for emergency assessment at the review
    iv("tuina", "procedure",
       L("推拿：腰部椎旁肌放松手法15分钟", "Tuina: 15 minutes of relaxing techniques to the lumbar paraspinal muscles"),
       KW(["推拿", "按摩", "揉法", "滚法"], ["tuina", "massage", "soft tissue", "manual therapy"]),
       dose=L("以滚法、揉法放松腰部椎旁肌，力度以患者可耐受为度，随时询问感受。", "Rolling and kneading techniques to relax the lumbar paraspinal muscles, at a pressure he finds tolerable, checking in with him throughout."),
       scope="medical", risk="low", checklist=True, maxDoses=1,
       contraindicatedWhen={"any": [{"not": {"all": [{"decided": "d-disease"}, {"decided": "d-pattern"}, {"intervened": "explain-consent"}]}}, {"phase": "followup"}]},
       harm=L("初诊时，推拿前要先完成危险信号筛查与诊断、辨证，再说明手法并征得同意。复诊时出现新的神经系统危险信号，任何手法治疗都要等急诊评估之后。",
              "At the first visit, tuina needs the danger-sign screen and diagnosis and the pattern assessment, then an explanation of the technique and his agreement. At the review, with new neurological danger signs, any manual therapy waits until he has been assessed in the Emergency Department."),
       response=L("推拿后他说腰部松了一些。", "After the tuina he says his back feels a little looser.")),
]

DECISIONS = [
    {
        "id": "d-followup", "kind": "single",
        "prompt": L("复诊时出现了新的症状与体征。你现在怎么处理？", "New symptoms and signs have appeared since last week. What do you do now?"),
        "requires": {"all": [{"asked": "h-fu-status"}, {"asked": "h-fu-redflags"}, {"examined": "e-fu-neuro"}]},
        "need": L("先问清楚这一周的变化和危险信号，并复查下肢神经系统。", "First ask what has changed this week and about the danger signs, and repeat the lower-limb neurological examination."),
        "options": [
            opt("transfer", True,
                L("疑似马尾综合征：今天停止中医治疗，立即转往急诊（当天评估与急诊MRI），并附书面交接",
                  "Suspected cauda equina syndrome: stop TCM treatment today and transfer him at once to an Emergency Department for same-day assessment and an emergency MRI, with a written handover"),
                L("正确。双下肢坐骨神经痛伴鞍区麻木和新出现的排尿费力，在急诊MRI排除之前都按疑似马尾综合征处理。结局取决于在尿潴留出现前减压，每一小时都重要；膀胱扫描、肛门指检和MRI由急诊完成，不在诊所。",
                  "Correct. Bilateral sciatica with saddle numbness and new difficulty passing urine is suspected cauda equina syndrome until an emergency MRI says otherwise. The outcome depends on decompression before retention sets in, so every hour counts; the bladder scan, rectal examination and MRI are done in the Emergency Department, not the clinic.")),
            opt("needle-review", False,
                L("坐骨神经痛发作：今天针刺止痛，三天后复诊", "A flare of sciatica: needle today for pain relief and review in three days"),
                L("不对。鞍区麻木和排尿费力不是普通的坐骨神经痛。针刺和等待三天会错过减压的时间窗。",
                  "No. Saddle numbness and difficulty passing urine are not ordinary sciatica. Needling and waiting three days lose the window for decompression.")),
            opt("routine-mri", False,
                L("转介综合诊所做MRI，期间继续服中药", "Refer to the polyclinic for an MRI and continue the herbs meanwhile"),
                L("不对。常规转介要几周；疑似马尾综合征需要经急诊在数小时内完成急诊MRI。",
                  "No. A routine referral takes weeks; suspected cauda equina syndrome needs an emergency MRI within hours through the Emergency Department.")),
            opt("stasis", False,
                L("新出现的刺痛属瘀血，改用更强的活血化瘀方，下周复诊", "The new stabbing pain is blood stasis: switch to a stronger blood-activating formula and review next week"),
                L("不对。证候也许变了，但危险信号优先于辨证。他服阿司匹林、又吃了布洛芬，可能还要手术，此时加强活血更增加出血风险。",
                  "No. The pattern may have changed, but danger signs outrank the pattern. With aspirin, ibuprofen and possible surgery ahead, stronger blood-activating herbs add bleeding risk.")),
            opt("wait-retention", False,
                L("嘱卧床休息，如完全解不出小便再来", "Advise bed rest and to come back if he cannot pass urine at all"),
                L("不对。等到完全尿潴留，就是在等结局更差的阶段（伴尿潴留的马尾综合征）。",
                  "No. Waiting for complete retention means waiting for the stage with the worse outcome (cauda equina syndrome with retention).")),
        ],
    }
]

OBJECTIVES = [
    {"id": "o-followup", "title": L("一周复诊：重新评估，并对变化作出处理", "One-week review: reassess and act on what has changed"),
     "short": L("复诊", "Review"),
     "hint": L("先问这一周有什么变化，再把危险信号重新问一遍、复查神经系统，然后按你的发现处理。",
               "Ask what has changed this week, go through the danger signs again and repeat the neurological examination, then act on what you find."),
     "guidance": L("在诊室与陈先生复诊。", "Review Mr Tan in the consulting room."),
     "completeWhen": {"all": [{"decided": "d-followup"}, {"intervened": "refer-ed", "valid": True}, {"intervened": "handover-letter", "valid": True}]},
     "waypoints": [{"target": "patient"}]},
]

RUBRIC = [
    {"id": "r-review-assessment", "domain": "history", "weight": 3,
     "text": L("复诊时重新筛查危险信号，问清起病时间与用药，并复查神经系统与直腿抬高",
               "At review, re-screened for danger signs, established when they began and what he had taken, and repeated the neurological examination and straight-leg raise"),
     "met": {"all": [{"asked": "h-fu-redflags"}, {"asked": "h-fu-onset-time"}, {"asked": "h-fu-meds-last"}, {"examined": "e-fu-neuro"}, {"examined": "e-fu-slr"}]}},
    {"id": "r-recognise", "domain": "diagnosis", "weight": 3, "critical": True,
     "text": L("首次即识别疑似马尾综合征并选择立即转诊", "Recognised suspected cauda equina syndrome and chose immediate transfer, first time"),
     "met": {"decidedFirstTry": "d-followup"}},
    {"id": "r-transfer", "domain": "management", "weight": 3, "critical": True,
     "text": L("复诊当天即转往急诊", "Transferred him to the Emergency Department the same day"),
     "met": {"intervened": "refer-ed", "valid": True}},
    {"id": "r-handover", "domain": "management", "weight": 2,
     "text": L("书面交接：症状及时间、体征、用药（含阿司匹林与布洛芬最后剂量）、已做的中医治疗",
               "Wrote a handover: symptoms and their times, signs, medicines (with the last doses of aspirin and ibuprofen) and the TCM treatment given"),
     "met": {"intervened": "handover-letter", "valid": True}},
    {"id": "r-stop-tcm", "domain": "safety", "weight": 2,
     "text": L("暂停中药和针灸，等待急诊评估", "Paused the herbs and acupuncture pending emergency assessment"),
     "met": {"intervened": "stop-tcm", "valid": True}},
    {"id": "r-no-delay", "domain": "safety", "weight": 3,
     "text": L("没有试图以针刺、推拿、继续疗程、观察等待、改方或常规转介代替急诊转诊（被拒绝的尝试也计入）",
               "Did not try to treat or wait instead of transferring — needling, tuina, a continued course, watchful waiting, a new formula or a routine referral (refused attempts included)"),
     "met": {"not": {"any": REFUSED_DELAYS + [{"intervened": "refer-imaging", "valid": False}]}},
     "scoredWhen": {"any": [{"phase": "followup"}] + REFUSED_DELAYS + [{"intervened": "refer-imaging"}]}},
    {"id": "r-comm-escalation", "domain": "communication", "weight": 1,
     "text": L("清楚而不惊吓地说明为什么必须马上去急诊", "Explained clearly, without alarming him, why he must go to the Emergency Department now"),
     "judgeGuidance": L("学员是否用通俗的语言说明这些新症状可能是神经受压、为什么今天就要做检查、到急诊后大概会发生什么；确认他如何安全到达（救护车）、是否通知家人，并交代路上如有加重怎么办？",
                        "Did the learner explain in plain words that the new symptoms may mean pressure on the nerves, why tests are needed today and roughly what will happen at the Emergency Department; check how he will get there safely (an ambulance) and whether his family is told; and say what to do if things get worse on the way?")},
]

SAFETY_GATES = [
    # One policy for comparable acts. Safety-critical: the decision to delay (a delaying plan chosen at the review
    # decision — every wrong option there delays), or a delaying act actually carried out (a routine referral sent).
    # Complication: a treatment or waiting plan attempted and refused — not given, transfer not held up.
    {"id": "g-delayed-emergency-care", "verdict": "safety-critical", "capPercent": 40,
     "label": L("出现疑似马尾综合征征象后决定拖延急诊处理（复诊决策选择了拖延的方案，或已发出常规转介）",
                "Emergency care delayed after signs of suspected cauda equina syndrome (a delaying plan chosen at the review decision, or a routine referral sent)"),
     "when": {"any": [{"all": [{"attempted": "d-followup"}, {"not": {"decidedFirstTry": "d-followup"}}]}, {"intervened": "refer-imaging", "valid": False}]}},
    {"id": "g-delay-refused", "verdict": "complication",
     "label": L("试图以中医治疗或等待代替急诊转诊（被拒绝，未执行，转诊未被耽搁）",
                "Treatment or waiting attempted instead of emergency transfer (refused: not given, and the transfer was not held up)"),
     "when": {"any": REFUSED_DELAYS}},
    {"id": "g-transfer-without-handover", "verdict": "complication",
     "label": L("转诊时没有书面交接", "Transferred without a written handover"),
     "when": {"all": [{"intervened": "refer-ed", "valid": True}, {"not": {"intervened": "handover-letter", "valid": True}}]}},
]

SOLUTION = [
    *ask("h-fu-status", "h-fu-redflags", "h-fu-onset-time", "h-fu-bowel", "h-fu-meds-last", "h-fu-adverse"),
    *examine("e-fu-general", "e-fu-neuro", "e-fu-slr", "e-fu-abdomen", "e-fu-lumbar"),
    answer("d-followup", "transfer"),
    *intervene("stop-tcm", "refer-ed", "handover-initial", "handover-letter"),
    {"type": "finish"},
]

UTTERANCES = [
    U("这一周腰怎么样？", "zh-CN", "h-fu-status"),
    U("how have things been since last week?", "en", "h-fu-status"),
    U("现在腿有没有麻、没力气？", "zh-CN", "h-fu-redflags"),
    U("any change in how your bladder feels?", "en", "h-fu-redflags"),
    U("麻木是什么时候开始的？", "zh-CN", "h-fu-onset-time", also=["h-fu-redflags"]),
    U("what time did the numbness come on?", "en", "h-fu-onset-time", also=["h-fu-redflags"]),
    U("最后一次吃阿司匹林是几点？", "zh-CN", "h-fu-meds-last"),
    # the audit's own questions (2026-11-12), verbatim; and negated forms
    U("会阴部感觉麻木吗？", "zh-CN", "h-fu-redflags"),
    U("你现在小便解得出来吗？", "zh-CN", "h-fu-redflags"),
    U("小便时要使劲才能尿出来吗？", "zh-CN", "h-fu-redflags"),
    U("擦屁股时，纸碰到皮肤的感觉跟平时一样吗？", "zh-CN", "h-fu-redflags"),
    U("有尿意但尿不出来吗？", "zh-CN", "h-fu-redflags"),
    U("排尿困难吗？", "zh-CN", "h-fu-redflags"),
    U("两条腿都痛到脚底吗？", "zh-CN", "h-fu-status"),
    U("小便没有问题吧？", "zh-CN", "h-fu-redflags"),
    U("下面不会麻吧？", "zh-CN", "h-fu-redflags"),
    U("you're not having to strain to pass urine, are you?", "en", "h-fu-redflags"),
    U("no numbness down below when you wipe?", "en", "h-fu-redflags"),
    U("have you taken any painkillers?", "en", "h-fu-meds-last"),
    U("上一次大便是什么时候？", "zh-CN", "h-fu-bowel"),
    U("when did you last open your bowels?", "en", "h-fu-bowel"),
]

OUTCOME = L("复诊时识别疑似马尾综合征的新征象，停止中医治疗并立即安排急诊转诊，附完整的书面交接（包括抗血小板药、止痛药及其最后剂量）。",
            "At review, recognise new signs of suspected cauda equina syndrome, stop TCM treatment and arrange immediate emergency transfer with a complete written handover (including antiplatelet and analgesic medicines and their last doses).")

DEBRIEF = {
    "title": L("复盘：复发性腰痛——复诊时出现危险信号", "Debrief: recurrent low back pain — danger signs at the review"),
    "conclusion": L(
        "初诊同 tcm-sg-lbp-01：非特异性腰痛，证属寒湿痹阻、兼肝肾不足，处方经审方修订后调剂，完成首次针灸。复诊时，他在搬重物后出现双下肢放射痛、鞍区麻木和排尿费力：疑似马尾综合征。正确的处理是今天停止中医治疗，立即转往急诊做急诊MRI，并附书面交接——症状及出现时间、体征、阿司匹林和布洛芬及其最后剂量、已用的中药和针灸。此时没有任何证候问题比这更重要。",
        "First visit as in tcm-sg-lbp-01: non-specific low back pain, cold-damp obstruction with liver–kidney insufficiency, a prescription revised after the dispensary's query, and a first acupuncture session. At the review, after lifting at work, he has pain down both legs, saddle numbness and difficulty passing urine: suspected cauda equina syndrome. The right care is to stop TCM treatment today and transfer him at once for an emergency MRI, with a written handover — the symptoms and when they began, the signs, his aspirin and ibuprofen with their last doses, and the herbs and acupuncture already given. No pattern question outranks that.",
    ),
    "keyReasoning": base.DEBRIEF["keyReasoning"][:4] + [
        L("每次复诊都要重新筛查危险信号：随访分支可以改变问题本身。一旦出现危险信号，要决定的是照护转移，而不是证候。",
          "Re-screen the danger signs at every review: a follow-up branch can change the question itself. Once they appear, the decision is about a care transition, not the pattern."),
    ],
    "teachingPoints": base.DEBRIEF["teachingPoints"] + [
        L("疑似马尾综合征（双侧坐骨神经痛、鞍区感觉减退、膀胱、肠道或性功能障碍）需立即转诊做急诊MRI；不要等到完全尿潴留（参见英国GIRFT全国疑似马尾综合征路径，2023）。",
          "Suspected cauda equina syndrome (bilateral sciatica, saddle sensory loss, bladder, bowel or sexual dysfunction) needs immediate referral for an emergency MRI; do not wait for complete retention (see the GIRFT national suspected cauda equina syndrome pathway, 2023)."),
    ],
    "references": base.REFERENCES + [
        "Getting It Right First Time (NHS England). National suspected cauda equina syndrome (CES) pathway. London: GIRFT; 2023.",
    ],
}


def build() -> dict:
    c = lbp_family.variant(
        case_id=CASE_ID,
        version="0.2.0",
        variant_id="review-b-escalation",
        title=L("腰痛反复发作 · 52岁男性 · 复诊B", "Recurrent low back pain · 52-year-old man · review B"),
        outcome=OUTCOME,
        review={"history": HISTORY, "exam": EXAM, "interventions": INTERVENTIONS, "decisions": DECISIONS, "objectives": OBJECTIVES,
                "rubric": RUBRIC, "safetyGates": SAFETY_GATES, "solution": SOLUTION, "utterances": UTTERANCES,
                "unknowns": [L("转诊后的MRI结果与急诊处理。", "The MRI result and the Emergency Department's management after transfer.")]},
        debrief=DEBRIEF,
        tcmcraft={
            "dates": dates("2026-11-07"),
            "unacceptable": ["rx-verbal-swap", "stop-aspirin", *DELAYS, "refer-imaging (at the review)", "tuina (at the review)"],
            "followUpModel": "authored branch: new neurological danger signs at the review (not a calibrated outcome model)",
        },
    )
    c["debrief"]["notice"] = base.DEBRIEF["notice"]
    return c
