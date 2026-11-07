"""Case tcm-sg-insomnia-02 — family sg-insomnia, review B: the watch and the diary disagree; a hypnotic in use.

The first visit is tcm-sg-insomnia-01's, unchanged. A week later her daughter gave her a smartwatch. Its app reports
about 6 h 50 min of sleep a night, "only 38 minutes of deep sleep" and a sleep score in the 50s ("poor"), while the
diary she fills in each morning — before she looks at the watch — shows about 5 h 20 min. Chasing the app's deep
sleep, she has gone to bed at eleven and stayed in bed late, giving up the sleep schedule. Worried by the score, she
saw a private GP near her office, who prescribed zolpidem 10 mg at bedtime. She has taken it for six nights,
together with the bedtime sachet of the sedating granules. Twice she was very unsteady at 3 a.m. getting up for her
mother-in-law (she walked into a door frame and bruised her shoulder), and she is groggy until mid-morning, when she
has already driven to work. Her polyclinic GP found iron-deficiency anaemia, as in review A; she takes the iron
correctly.

Phase 2 dimensions: uncertain evidence (two sources that disagree, of different quality) and a herb–drug review.
The learner weighs the sources, keeps the diary as the working measure, resets the schedule, changes what is theirs
(holds the bedtime sachet), counsels on night and morning safety, and contacts the prescriber the same day rather
than stopping someone else's medicine or adding more sedation (cinnabar, 朱砂, is refused and gated).

Synthetic: no real patient, no source report.
"""

from __future__ import annotations

import copy

import case_insomnia as base
import insomnia_family
from case_lbp import KW, L, U, answer, ask, ex, examine, hx, intervene, iv, opt, order_read

CASE_ID = "tcm-sg-insomnia-02"
REVIEW = ["review"]
AUTHORED = base.AUTHORED

HISTORY = [
    hx("h-rv-status", "hpi",
       L("这两个星期睡得怎么样？", "How have you been sleeping these two weeks?"),
       L("没有好，可能还更差。手表说我深睡只有三十几分钟，分数一直是“差”。早上起来头昏昏的，到十点左右才清醒。",
         "No better — maybe worse. The watch says I only get thirty-odd minutes of deep sleep, and my score is always \"poor\". I wake up muzzy-headed and don't feel clear until about ten."),
       KW(["这两个星期", "这两周", "睡得怎么样", "有没有好转", "上次以后"], ["these two weeks", "past two weeks", "sleeping now", "any better", "since last time"]),
       required=True, phases=REVIEW, supersedes=["h-presenting", "h-sleep-pattern", "h-daytime"],
       exclude=KW(["心情", "情绪", "手表", "新的药", "日记", "医生"], ["mood", "watch", "new medicine", "diary", "doctor"])),
    hx("h-rv-watch", "other",
       L("手表是怎么回事？它显示什么？", "Tell me about the watch — what does it show?"),
       L("女儿上个星期送我的智能手表。它说我平均睡六个钟头五十分，可是深睡只有三十八分钟，睡眠分数五十几分，写着“差”。我每天早上一起床就看。",
         "My daughter gave me a smartwatch last week. It says I sleep six hours fifty on average, but only thirty-eight minutes of deep sleep, and my sleep score is in the fifties — it says \"poor\". I check it the moment I wake up."),
       KW(["手表", "智能手表", "手环", "深睡", "睡眠分数"], ["watch", "smartwatch", "tracker", "deep sleep", "sleep score"]),
       required=True, phases=REVIEW),
    hx("h-rv-cbti", "functional",
       L("睡眠计划有没有照着做？", "Have you kept to the sleep plan?"),
       L("第一个星期有照做，六点半起床、十二点四十五分才上床，其实睡得比较好。有了手表以后，app说要多一点深睡，我就十一点上床，能睡就睡到七点半。",
         "The first week I did — up at half past six, not in bed till a quarter to one — and actually I slept better. Since the watch, the app says I need more deep sleep, so I go to bed at eleven and lie in till half past seven when I can."),
       KW(["睡眠计划", "有没有照着做", "按计划", "计划做得"], ["sleep plan", "stick to the plan", "kept to the plan", "keep to the schedule"]),
       required=True, phases=REVIEW),
    hx("h-rv-diary-method", "other",
       L("睡眠日记是什么时候写的？", "When do you fill in the sleep diary?"),
       L("每天早上起床就写，在看手表之前。照你说的，写大概几点上床、多久睡着、醒了多久。",
         "Every morning as soon as I get up, before I look at the watch. As you told me — roughly when I went to bed, how long it took to fall asleep, how long I was awake."),
       KW(["什么时候写", "日记怎么写", "怎么记日记", "写日记"], ["fill in the diary", "how do you keep the diary", "write the diary"]),
       phases=REVIEW),
    hx("h-rv-meds", "medications",
       L("这两个星期有没有开始吃什么新的药？有没有看别的医生？", "Have you started any new medicines these two weeks, or seen another doctor?"),
       L("啊，有。手表分数一直差，我很担心，上个星期去了公司附近的诊所，医生开了安眠药，zolpidem 10毫克，睡前吃一粒，开了十四粒。吃了六个晚上，跟睡前那包中药一起吃。还有综合诊所开的铁片。",
         "Oh — yes. The watch score kept saying poor and I was worried, so last week I went to a clinic near my office, and the doctor gave me sleeping tablets — zolpidem 10 mg, one at bedtime, fourteen tablets. I've taken it six nights, with the bedtime sachet of the herbs. And the iron from the polyclinic."),
       KW(["新的药", "新药", "别的医生", "其他医生", "最近开始吃", "别的诊所"], ["new medicines", "new medication", "started any", "another doctor", "other doctor", "another clinic"]),
       required=True, phases=REVIEW, supersedes=["h-meds"]),
    hx("h-rv-night-events", "other",
       L("吃了药以后，晚上起来有没有站不稳、跌倒，或者做了事情自己不记得？", "After the tablet, have you been unsteady, fallen, or done anything at night you can't remember?"),
       L("有两个晚上三点多婆婆起来走动，我起来看她，脚步很不稳，有一次撞到门框，左肩膀瘀青了。没有跌倒。没有做过自己不记得的事。",
         "Twice, at about three, my mother-in-law got up and wandered and I got up for her — I was very unsteady, and once I walked into the door frame and bruised my left shoulder. I didn't fall. I haven't done anything I can't remember."),
       KW(["站不稳", "跌倒", "摔倒", "撞到", "不记得", "晚上起来"], ["unsteady", "fallen", "fall", "can't remember", "sleepwalking", "at night after the tablet"]),
       required=True, phases=REVIEW, safety={"datum": "night-falls", "finding": "near-fall"}),
    hx("h-rv-morning", "functional",
       L("早上起来精神怎么样？怎么去上班？", "How are you in the mornings, and how do you get to work?"),
       L("早上头昏昏的，反应慢，到十点才清醒。我每天自己开车上班，大概七点四十出门。",
         "Muzzy and slow in the mornings, not clear till ten. I drive myself to work every day — I leave about twenty to eight."),
       KW(["早上", "开车", "上班", "头昏", "反应慢"], ["mornings", "drive", "driving", "groggy", "commute"]),
       required=True, phases=REVIEW),
    hx("h-rv-iron", "medications",
       L("铁片是怎么吃的？", "How are you taking the iron?"),
       L("综合诊所的药剂师交代过：早上起床空腹用水吃，过两个钟头才喝奶茶、吃中药。黑便、有一点便秘，其他没事。",
         "The polyclinic pharmacist explained: on waking, on an empty stomach with water, and milk tea and the herbs only two hours later. Dark stools and a bit constipated, nothing else."),
       KW(["铁剂", "铁片", "补铁"], ["iron", "iron tablet", "iron supplement"]),
       phases=REVIEW),
    hx("h-rv-mood", "ros",
       L("这两个星期心情怎么样？有没有伤害自己的念头？", "How has your mood been these two weeks, and have you had any thoughts of harming yourself?"),
       L("一直盯着手表的分数，很焦虑。心情还可以，没有那种念头。", "I keep staring at the watch score and it makes me anxious. My mood's all right, and no thoughts like that."),
       KW(["心情", "情绪", "伤害自己", "念头"], ["mood", "feeling", "harming yourself", "thoughts"]),
       required=True, phases=REVIEW, supersedes=["h-mood", "h-suicide"]),
]

EXAM = [
    ex("e-rv-general", "general",
       L("复诊望神色", "Inspect her spirit and complexion again"),
       L("神疲，回答比上次慢；面色仍淡；左肩前方一块约3厘米的瘀青，活动正常，无骨压痛。", "Tired, slower to answer than last time; complexion still pale; a bruise about 3 cm across the front of the left shoulder, with full movement and no bony tenderness."),
       KW(["望诊", "面色", "精神", "瘀青"], ["inspect", "complexion", "general appearance", "bruise"]),
       abnormal=True, required=True, phases=REVIEW),
    ex("e-rv-balance", "neurological",
       L("观察步态，做闭目站立试验", "Watch her gait and do a Romberg test"),
       L("此刻（上午十一点）步态稳，闭目站立试验阴性。她说不稳只在夜里吃药后。", "Now (11 a.m.) her gait is steady and Romberg's test is negative. She says the unsteadiness is only at night after the tablet."),
       KW(["步态", "走路", "闭目站立", "平衡"], ["gait", "romberg", "balance"]),
       phases=REVIEW),
    ex("e-rv-tongue", "heent",
       L("复查舌象", "Re-inspect the tongue"),
       L("舌淡，齿痕同前；苔薄白。", "Pale, with the same tooth marks; coating thin and white."),
       KW(["舌", "舌象", "舌苔", "望舌"], ["tongue", "coating", "inspect the tongue"]),
       phases=REVIEW),
    ex("e-rv-pulse", "cardiovascular",
       L("复诊切脉", "Retake the pulse"),
       L("脉细弱，80次/分。", "Thready and weak, 80/min."),
       KW(["切脉", "把脉", "脉象"], ["pulse", "take the pulse"]),
       phases=REVIEW),
]

GP_RESULTS = copy.deepcopy(next(i for i in base.INVESTIGATIONS if i["id"] == "gp-results"))

INVESTIGATIONS = [
    {
        "id": "sleep-diary-review", "name": L("近两周的睡眠日记（复诊）", "Sleep diary for the last two weeks (review)"),
        "category": "record", "aliases": KW(["新的睡眠日记", "复诊睡眠日记", "这两周的日记"], ["new sleep diary", "review diary", "latest diary"]),
        "requires": ["records"], "risk": "none", "performedAt": "records", "value": "essential", "availability": {"historical": False},
        "results": {"review": {
            "date": L("过去两周（每天早上起床后、看手表前填写）", "The past two weeks (filled in each morning on rising, before looking at the watch)"),
            "text": L("第一周：06:30起床，00:45上床，卧床5小时45分；实际睡眠约5小时10分（睡眠效率约90%）。"
                      "第二周（开始戴手表、服安眠药）：23:00上床，06:30–07:30起床，卧床约8小时；入睡约25分钟，夜里醒着合计约2小时15分（包括起来照顾婆婆）；实际睡眠约5小时20分（睡眠效率约67%）。",
                      "Week 1: rising at 06:30, bed at 00:45, 5 h 45 min in bed; sleep about 5 h 10 min (sleep efficiency about 90%). "
                      "Week 2 (watch and sleeping tablet started): bed at 23:00, rising 06:30–07:30, about 8 hours in bed; about 25 minutes to fall asleep and about 2 h 15 min awake in the night (getting up for her mother-in-law included); sleep about 5 h 20 min (sleep efficiency about 67%)."),
            "source": AUTHORED}},
    },
    {
        "id": "watch-export", "name": L("智能手表应用程序的一周睡眠报告", "The smartwatch app's weekly sleep report"),
        "category": "record", "aliases": KW(["手表数据", "手表报告", "手环数据", "手表的记录"], ["watch data", "watch report", "tracker data", "the app report"]),
        "requires": ["records"], "risk": "none", "performedAt": "records", "value": "essential", "availability": {"historical": False},
        "results": {"review": {
            "date": L("过去7晚（第二周）", "The last 7 nights (week 2)"),
            "text": L("消费级腕戴设备，根据动作与心率推算。平均“在床”7小时55分，“睡眠”6小时50分（深睡38分钟、浅睡4小时52分、快速眼动1小时20分），“清醒”1小时05分；睡眠分数平均58/100（“差”）。应用程序说明：“本产品不是医疗器械，不用于诊断、治疗或预防任何疾病。”",
                      "A consumer wrist device that infers sleep from movement and heart rate. Average \"in bed\" 7 h 55 min, \"asleep\" 6 h 50 min (deep 38 min, light 4 h 52 min, REM 1 h 20 min), \"awake\" 1 h 05 min; average sleep score 58/100 (\"poor\"). The app's notice: \"This product is not a medical device and is not intended to diagnose, treat or prevent any disease.\""),
            "note": L("与同一周的日记相比，手表的睡眠时间多约1小时30分。", "Compared with the diary for the same week, the watch reports about 1 h 30 min more sleep."),
            "source": AUTHORED}},
    },
    {
        "id": "zolpidem-label", "name": L("查看她带来的安眠药药袋与标签", "Look at the sleeping-tablet bag and label she brought"),
        "category": "bedside", "aliases": KW(["安眠药药袋", "药袋", "药的标签", "看标签"], ["tablet label", "medicine bag", "the label", "zolpidem bag"]),
        "risk": "none", "performedAt": "bedside", "value": "essential",
        "results": {"review": {
            "date": L("七天前，私人诊所", "Seven days ago, a private clinic"),
            "text": L("“唑吡坦（zolpidem）10毫克 — 每晚睡前1粒 — 共14粒。可能引起嗜睡；服药后不可驾驶或操作机器；勿与酒同服。”开药医生：私人诊所的Rahman医生。袋内剩8粒。",
                      "\"Zolpidem 10 mg — 1 tablet at bedtime — 14 tablets. May cause drowsiness; do not drive or operate machinery after taking; avoid alcohol.\" Prescriber: Dr Rahman, a private clinic. Eight tablets left in the bag."),
            "source": AUTHORED}},
    },
    GP_RESULTS,
]

IN_REVIEW = {"phase": "review"}
KNOWS_HYPNOTIC = {"all": [IN_REVIEW, {"asked": "h-rv-meds"}]}

INTERVENTIONS = [
    iv("watch-explain", "other",
       L("解释手表能测和不能测什么：日记仍是治疗依据；接下来四周晚上不戴手表（或隐藏睡眠分数）",
         "Explain what the watch can and cannot measure: the diary stays the measure for treatment; no watch at night (or the sleep score hidden) for the next four weeks"),
       KW(["解释手表", "手表不准", "不要戴手表", "隐藏分数", "手表的局限"], ["explain the watch", "watch limits", "take the watch off", "hide the score", "not a medical device"]),
       risk="none", checklist=True, setFlags=["watch-explained"],
       contraindicatedWhen={"not": {"all": [IN_REVIEW, {"asked": "h-rv-watch"}]}},
       harm=L("先问清楚手表的情况。", "Find out about the watch first."),
       response=L("她有点意外：“所以躺着不动它也算我睡着？”她同意先把手表收进抽屉，日记照写。", "She is surprised: \"So if I lie still it counts me as asleep?\" She agrees to put the watch in a drawer at night and keep writing the diary.")),
    iv("restriction-reset", "other",
       L("恢复睡眠时间表：06:30起床，00:30上床（卧床6小时，第一周已达到可延长15分钟的标准），醒着就离床，每天早上写日记",
         "Restart the sleep schedule: rise at 06:30, bed at 00:30 (6 hours in bed — the 15-minute step her first week had earned), out of bed when awake, the diary each morning"),
       KW(["恢复睡眠计划", "重新开始睡眠限制", "回到原来的时间表", "不要提早上床"], ["restart the schedule", "back to the sleep plan", "reset the schedule", "no early nights"]),
       risk="none", checklist=True, setFlags=["schedule-reset"],
       contraindicatedWhen={"not": IN_REVIEW},
       harm=L("还没有时间表可以恢复。", "There is no schedule to restart yet."),
       response=L("她看着自己第一周的日记：“那一周其实睡得最好。”她把起床和上床时间重新写进手机备忘。", "She looks at her own first-week diary: \"That was actually my best week.\" She puts the rising and bed times back into her phone.")),
    iv("hold-evening-sachet", "medication",
       L("记录一项临时调整：服用唑吡坦期间暂停睡前那包中药，午饭后那包照服，并告知开药医生",
         "Record a temporary change: hold the bedtime sachet while she takes zolpidem, keep the after-lunch sachet, and tell the prescriber"),
       KW(["暂停睡前那包", "睡前不要吃中药", "停晚上那包", "只吃午饭那包"], ["hold the bedtime sachet", "skip the evening sachet", "stop the bedtime herbs", "lunchtime sachet only"]),
       requires=["records"], scope="medical", risk="none", checklist=True, setFlags=["evening-sachet-held"],
       contraindicatedWhen={"not": KNOWS_HYPNOTIC},
       harm=L("先问清楚她最近在吃的所有药。", "Find out everything she is taking now first."),
       response=L("病历已记录：服用唑吡坦期间暂停睡前1包，午饭后1包照服；药房已在她的记录上注明。", "Recorded in the notes: bedtime sachet held while she takes zolpidem, after-lunch sachet unchanged; the dispensary has noted it on her record.")),
    iv("night-safety", "other",
       L("夜间与早上的安全建议：嗜睡时不开车，不喝酒；服药的晚上由先生负责照顾婆婆；夜灯、起身要慢",
         "Night and morning safety: no driving while drowsy, no alcohol; on nights she takes the tablet, her husband looks after his mother; a nightlight, and get up slowly"),
       KW(["安全建议", "不要开车", "嗜睡不开车", "夜灯", "先生照顾婆婆"], ["safety advice", "don't drive", "no driving", "nightlight", "husband takes the night"]),
       risk="none", checklist=True, setFlags=["night-safety"],
       contraindicatedWhen={"not": KNOWS_HYPNOTIC},
       harm=L("先问清楚她最近在吃的所有药。", "Find out everything she is taking now first."),
       response=L("她说可以先搭地铁上班，也会请先生这几个晚上起来照顾婆婆。", "She says she can take the MRT to work for now, and she'll ask her husband to get up for his mother on those nights.")),
    iv("prescriber-letter", "consult",
       L("当天联系开药的Rahman医生并附信：列出中药与剂量、夜间站不稳与撞伤、早上头昏仍开车、正在做的睡眠限制，请他评估唑吡坦的剂量与是否继续",
         "Contact Dr Rahman, who prescribed it, the same day, with a letter: the herbs and doses, the night-time unsteadiness and the bruise, the morning grogginess while driving, and the sleep-restriction schedule; ask him to review the zolpidem dose and whether to continue"),
       KW(["联系开药医生", "写信给医生", "Rahman医生", "通知医生", "联系那位医生"], ["contact the prescriber", "prescriber letter", "call dr rahman", "write to the gp", "inform the prescriber"]),
       requires=["records"], scope="medical", risk="none", checklist=True, setFlags=["prescriber-contacted"],
       contraindicatedWhen={"not": KNOWS_HYPNOTIC},
       harm=L("先问清楚她最近在吃的所有药，以及是谁开的。", "Find out everything she is taking now, and who prescribed it, first."),
       response=L("下午Rahman医生回电：考虑到夜间不稳与她要照顾家人，他改为必要时5毫克、只在先生值夜的晚上服用，两周内停用；同意暂停睡前中药，并请她两周后回去复诊。他也说标签上写着服药后要能在床上睡足七到八小时，与睡眠限制时间表冲突，所以更要减少使用。",
                  "Dr Rahman calls back in the afternoon. Given the night-time unsteadiness and her caring at night, he changes it to 5 mg as needed, only on nights her husband is on duty, stopping within two weeks; he agrees with holding the bedtime herbs and asks to see her in two weeks. He adds that the label asks for seven to eight hours in bed after a dose, which clashes with her sleep-restriction schedule — another reason to use it less.")),
    iv("stop-zolpidem", "medication",
       L("叫她停用唑吡坦，改靠中药安神", "Tell her to stop the zolpidem and rely on the herbs instead"),
       KW(["停安眠药", "不要再吃安眠药", "停掉唑吡坦", "用中药代替安眠药"], ["stop the zolpidem", "stop the sleeping tablets", "herbs instead of the tablet", "no more sleeping pills"]),
       scope="medical", risk="moderate",
       contraindicatedWhen={"always": True},
       harm=L("这不是你开的药：开药医生今天就联系得到，剂量与是否停用应由他决定；中药也不能代替催眠药。你能改的是你自己的处方——暂停睡前那包——并把情况告诉他。",
              "It is not your prescription: the prescriber can be reached today, and the dose and whether to stop are his decision; nor do herbs replace a hypnotic. What you can change is your own prescription — hold the bedtime sachet — and tell him what has happened."),
       response=L("她不太确定该听谁的。", "She is unsure whose advice to follow.")),
    iv("add-cinnabar", "medication",
       L("她没有好转：加朱砂安神丸加强安神", "She is no better: add Zhu Sha An Shen Wan (cinnabar) to strengthen the sedation"),
       KW(["朱砂", "朱砂安神丸", "加强安神", "重镇安神"], ["cinnabar", "zhu sha", "zhu sha an shen", "stronger sedation"]),
       scope="medical", risk="high",
       contraindicatedWhen={"always": True},
       harm=L("朱砂为硫化汞：汞可蓄积，损害肾与神经系统；《中国药典》要求不宜大量服用、也不宜少量久服。她的问题也不是镇静不够，而是夜里已经镇静过度、时间表被打乱。",
              "Cinnabar is mercury sulphide: mercury accumulates and harms the kidneys and nervous system, and the Chinese Pharmacopoeia warns against large doses and against long use even of small ones. Nor is her problem too little sedation: she is already over-sedated at night, and her schedule has slipped."),
       response=L("处方已写好。", "The prescription is written.")),
    iv("extend-bed", "other",
       L("照手表的建议，让她早点上床、晚点起床，多补深睡", "As the app suggests, let her go to bed earlier and stay in bed later to catch up on deep sleep"),
       KW(["早点上床", "多躺一会", "补深睡", "睡久一点"], ["go to bed earlier", "stay in bed longer", "catch up on deep sleep", "more time in bed"]),
       risk="low",
       contraindicatedWhen={"always": True},
       harm=L("卧床越久，醒着躺在床上的时间越多：她的日记显示睡眠效率已从约90%降到约67%，实际睡眠并没有增加。这正好抵消了睡眠认知行为治疗。",
              "More time in bed means more time lying awake: her diary shows sleep efficiency down from about 90% to about 67%, with no more actual sleep. It undoes the CBT-I."),
       response=L("她看起来松了一口气。", "She looks relieved.")),
]

DECISIONS = [
    {"id": "d-sleep-evidence", "kind": "single",
     "prompt": L("手表说她每晚睡6小时50分，日记说5小时20分。怎么看这两份证据？", "The watch says she sleeps 6 h 50 min a night; the diary says 5 h 20 min. How do you weigh the two?"),
     "requires": {"all": [{"read": "sleep-diary-review", "phase": "review"}, {"read": "watch-export", "phase": "review"}, {"asked": "h-rv-watch"}, {"asked": "h-rv-diary-method"}]},
     "need": L("先看日记与手表报告，并问清楚手表的情况和日记是怎么写的。", "First read the diary and the watch report, and find out about the watch and how she keeps the diary."),
     "options": [
         opt("diary", True,
             L("以日记（每天早上、看手表前写）作为治疗依据，谨慎看待手表：消费级手表靠动作与心率推算，失眠者躺着不动常被算作睡着，深睡与分数也不可靠。两者都不是“真值”，差距本身有意义；而手表已经让她卧床更久",
               "Use the diary — kept each morning before she looks at the watch — as the working measure, and read the watch with caution: a consumer tracker infers sleep from movement and heart rate, so lying still awake often counts as sleep in insomnia, and its deep-sleep and score figures are unreliable. Neither is ground truth, and the gap itself is informative — and the watch has already lengthened her time in bed"),
             L("正确。消费级睡眠追踪器与多导睡眠图相比，常高估总睡眠、低估夜间清醒，对睡眠分期也不准，对失眠者尤其如此。失眠者也可能低估自己的睡眠，所以真实值可能介于两者之间，但治疗靠的是一致方法记录的日记、白天功能与行为。她为了追分数而延长卧床，睡眠效率从约90%降到约67%——这是手表带来的真实伤害。",
               "Correct. Against polysomnography, consumer sleep trackers tend to overestimate total sleep, underestimate waking in the night and stage sleep poorly, especially in insomnia. People with insomnia may also underestimate their sleep, so the truth may lie between; but treatment rests on a diary kept the same way each day, daytime function and behaviour. Chasing the score, she has lengthened her time in bed and her sleep efficiency has fallen from about 90% to about 67% — a real harm the watch has caused.")),
         opt("watch", False,
             L("手表是客观数据：她其实睡了快7个小时，是睡眠感知错误——安慰她，逐步结束治疗", "The watch is objective: she actually sleeps nearly 7 hours — sleep-state misperception; reassure her and wind treatment down"),
             L("不对。消费级手表不是经过失眠验证的测量工具，往往把安静的清醒算成睡眠。失眠者确实可能低估睡眠，但这不等于没有失眠：她白天功能受损，日记也是一致记录的。",
               "No. A consumer watch is not a measure validated in insomnia, and tends to count quiet waking as sleep. People with insomnia can underestimate their sleep, but that does not mean there is no insomnia: her days are impaired, and the diary is kept consistently.")),
         opt("psg", False,
             L("安排多导睡眠图，看谁对", "Arrange polysomnography to settle which is right"),
             L("不对。失眠评估一般不需要多导睡眠图，除非怀疑其他睡眠障碍（她STOP-Bang 1分，没有打鼾或腿部不适）；结果也不会改变方案。真需要客观估计时，常用的是体动记录仪配合日记。",
                "No. Polysomnography is not needed to assess insomnia unless another sleep disorder is suspected (her STOP-Bang is 1, with no snoring or restless legs), and it would not change the plan. When an objective estimate is really needed, actigraphy with the diary is the usual tool.")),
         opt("average", False,
             L("两者取平均（约6小时），照原方案继续", "Average the two (about 6 hours) and carry on as before"),
             L("不对。把两个偏差不同的估计平均，得到的并不是更准的测量；而且这样会漏掉真正的问题：手表已经改变了她的作息。",
               "No. Averaging two estimates with different biases does not make a better measure, and it misses the real problem: the watch has changed what she does.")),
     ]},
    {"id": "d-review", "kind": "single",
     "prompt": L("她在服唑吡坦10毫克，与睡前的安神中药同服。现在怎么处理？", "She is taking zolpidem 10 mg together with the bedtime sachet of sedating herbs. What now?"),
     "requires": {"all": [{"asked": "h-rv-meds"}, {"asked": "h-rv-night-events"}, {"asked": "h-rv-morning"}, {"read": "zolpidem-label", "phase": "review"}]},
     "need": L("先问清楚新开的药、夜里的情况和早上的状态，并看药袋标签。", "First find out about the new medicine, the nights and the mornings, and look at the label."),
     "options": [
         opt("coordinate", True,
             L("药物—中药核查：唑吡坦10毫克加睡前安神中药后，夜里站不稳撞伤、早上头昏仍开车。改你自己能改的（暂停睡前那包），给夜间和早上的安全建议，当天联系开药医生并附中药清单、事件与睡眠时间表；不自行停用或改动他的药；恢复睡眠时间表",
               "Herb–drug review: zolpidem 10 mg with the bedtime sachet of sedating herbs has been followed by unsteadiness and a knock at night and by grogginess while she drives. Change what is yours (hold the bedtime sachet), give night and morning safety advice, and contact the prescriber the same day with the herb list, the events and the sleep schedule; do not stop or change his medicine yourself; restart the sleep schedule"),
             L("正确。酸枣仁、远志、合欢皮有安神作用，与唑吡坦同用可能加重镇静，虽然相互作用的直接证据有限，谨慎起见先暂停睡前那包。唑吡坦有次日残留作用，美国FDA建议女性起始剂量为5毫克，并就复杂睡眠行为加了黑框警示；标签要求服药后能在床上待足7–8小时，这与睡眠限制冲突。夜里还要照顾失智的婆婆，跌倒风险真实存在。剂量与是否继续由开药医生决定——你要做的是让他今天就知道这些。",
               "Correct. 酸枣仁, 远志 and 合欢皮 are calming herbs, and with zolpidem they may add to sedation; direct evidence of an interaction is limited, so the bedtime sachet is held as a precaution. Zolpidem has next-morning effects: the US FDA recommends a 5 mg starting dose for women and has a boxed warning about complex sleep behaviours, and the label asks for 7–8 hours in bed after a dose, which clashes with sleep restriction. She also gets up at night for a mother-in-law with dementia, so the fall risk is real. The dose and whether to continue are the prescriber's decision — your job is to make sure he knows all this today.")),
         opt("herbs-instead", False,
             L("叫她停用唑吡坦，改靠中药", "Tell her to stop the zolpidem and rely on the herbs"),
             L("不对。这不是你开的药，开药医生今天联系得到；中药也不能代替催眠药。你能改的是自己的处方，并把情况告诉他。",
               "No. It is not your prescription, and the prescriber can be reached today; nor do herbs replace a hypnotic. Change your own prescription and tell him what has happened.")),
         opt("cinnabar", False,
             L("她没有好转：加朱砂安神丸加强安神", "She is no better: add Zhu Sha An Shen Wan (cinnabar) to strengthen the sedation"),
             L("不对。朱砂含汞，有蓄积毒性；她也不是镇静不够，而是夜里已经镇静过度、时间表被打乱。", "No. Cinnabar contains mercury, which accumulates; and she is not under-sedated — she is over-sedated at night and her schedule has slipped.")),
         opt("unchanged", False,
             L("没有什么相互作用要担心，全部照旧", "There is no interaction to worry about: carry on with everything as it is"),
             L("不对。睡前同服两种镇静的东西之后，夜里已经站不稳撞伤，早上头昏还开车——这需要今天处理。", "No. Since taking two sedating things at bedtime she has been unsteady and hurt herself at night, and drives while groggy — this needs dealing with today.")),
     ]},
]

OBJECTIVES = [
    {"id": "o-review", "title": L("两周复诊：权衡手表与日记，核查新开的安眠药", "Two-week review: weigh the watch against the diary, and review the new sleeping tablet"),
     "short": L("复诊", "Review"),
     "hint": L("看日记和手表报告，问清楚日记怎么写、手表怎么说；再问她最近有没有开始吃新的药、看过别的医生。",
               "Read the diary and the watch report, and find out how she keeps the diary and what the watch says; then ask whether she has started any new medicine or seen another doctor."),
     "completeWhen": {"all": [{"decided": "d-sleep-evidence"}, {"decided": "d-review"}, {"intervened": "watch-explain", "valid": True},
                              {"intervened": "restriction-reset", "valid": True}, {"intervened": "hold-evening-sachet", "valid": True},
                              {"intervened": "night-safety", "valid": True}, {"intervened": "prescriber-letter", "valid": True}]},
     "waypoints": [{"unless": {"read": "watch-export"}, "target": "records"}, {"target": "patient"}]},
]

HARMS = ["stop-zolpidem", "add-cinnabar", "extend-bed"]

RUBRIC = [
    {"id": "r-review-inquiry", "domain": "history", "weight": 3,
     "text": L("复诊问清：睡眠、手表、计划执行、日记写法、新药、夜间事件、早上与开车、情绪", "At review, established her sleep, the watch, the plan, how the diary is kept, new medicines, night events, mornings and driving, and mood"),
     "met": {"all": [{"asked": h} for h in ["h-rv-status", "h-rv-watch", "h-rv-cbti", "h-rv-diary-method", "h-rv-meds", "h-rv-night-events", "h-rv-morning", "h-rv-mood"]]}},
    {"id": "r-review-records", "domain": "investigations", "weight": 1,
     "text": L("看了日记、手表报告和安眠药标签", "Read the diary, the watch report and the sleeping-tablet label"),
     "met": {"all": [{"read": "sleep-diary-review"}, {"read": "watch-export"}, {"read": "zolpidem-label"}]}},
    {"id": "r-evidence", "domain": "diagnosis", "weight": 3, "critical": True,
     "text": L("首次即正确权衡手表与日记", "Weighed the watch against the diary correctly first time"),
     "met": {"decidedFirstTry": "d-sleep-evidence"}},
    {"id": "r-hypnotic-review", "domain": "management", "weight": 3, "critical": True,
     "text": L("首次即正确处理安眠药与中药同用，并当天联系开药医生", "Handled the hypnotic with the herbs correctly first time, and contacted the prescriber the same day"),
     "met": {"all": [{"decidedFirstTry": "d-review"}, {"intervened": "prescriber-letter", "valid": True}]}},
    {"id": "r-own-herbs", "domain": "safety", "weight": 2,
     "text": L("改自己能改的：暂停睡前那包中药", "Changed what was hers to change: held the bedtime sachet"),
     "met": {"intervened": "hold-evening-sachet", "valid": True}},
    {"id": "r-night-safety", "domain": "safety", "weight": 2,
     "text": L("给了夜间与早上开车的安全建议", "Gave night-time and morning driving safety advice"),
     "met": {"intervened": "night-safety", "valid": True}},
    {"id": "r-reset", "domain": "management", "weight": 2,
     "text": L("解释手表的局限并恢复睡眠时间表", "Explained the watch's limits and restarted the sleep schedule"),
     "met": {"all": [{"intervened": "watch-explain", "valid": True}, {"intervened": "restriction-reset", "valid": True}]}},
    {"id": "r-no-harm-review", "domain": "safety", "weight": 2,
     "text": L("没有自行停用别人开的药、没有加朱砂、没有延长卧床", "Did not stop another prescriber's medicine, add cinnabar or lengthen her time in bed"),
     "met": {"not": {"any": [{"intervened": x} for x in HARMS]}},
     "scoredWhen": {"any": [IN_REVIEW] + [{"intervened": x} for x in HARMS]}},
    {"id": "r-comm-review", "domain": "communication", "weight": 1,
     "text": L("尊重她对手表的信任与担忧，不贬低她或另一位医生", "Respected her trust in the watch and her worry, without belittling her or the other doctor"),
     "judgeGuidance": L("学员是否先肯定她想弄清楚自己睡眠的用心，再解释手表的局限；是否不责怪她去看别的医生，也不批评那位医生；是否清楚说明为什么要暂停睡前中药、为什么暂时不开车、接下来谁会做什么决定？",
                        "Did the learner acknowledge her wish to understand her sleep before explaining the watch's limits; avoid blaming her for seeing another doctor or criticising that doctor; and explain clearly why the bedtime herbs are held, why she should not drive for now, and who decides what next?")},
]

SAFETY_GATES = [
    {"id": "g-cinnabar", "verdict": "safety-critical", "capPercent": 40,
     "label": L("对失眠患者加用含汞的朱砂", "Added mercury-containing cinnabar for insomnia"),
     "when": {"intervened": "add-cinnabar"}},
    {"id": "g-hypnotic-substitution", "verdict": "complication",
     "label": L("绕过开药医生，叫患者停用催眠药改服中药", "Told the patient to stop a hypnotic for herbs, bypassing the prescriber"),
     "when": {"intervened": "stop-zolpidem"}},
]

SOLUTION = [
    *ask("h-rv-status", "h-rv-watch", "h-rv-cbti", "h-rv-diary-method", "h-rv-meds", "h-rv-night-events", "h-rv-morning", "h-rv-iron", "h-rv-mood"),
    *examine("e-rv-general", "e-rv-balance", "e-rv-tongue", "e-rv-pulse"),
    *order_read("sleep-diary-review", "review"),
    *order_read("watch-export", "review"),
    *order_read("zolpidem-label", "review"),
    *order_read("gp-results", "review"),
    answer("d-sleep-evidence", "diary"),
    answer("d-review", "coordinate"),
    *intervene("watch-explain", "restriction-reset", "hold-evening-sachet", "night-safety", "prescriber-letter"),
    {"type": "finish"},
]

UTTERANCES = [
    U("这两周睡得怎么样？", "zh-CN", "h-rv-status"),
    U("are you sleeping any better these two weeks?", "en", "h-rv-status"),
    U("你的手表显示什么？", "zh-CN", "h-rv-watch"),
    U("what does your smartwatch say?", "en", "h-rv-watch"),
    U("睡眠计划有照着做吗？", "zh-CN", "h-rv-cbti"),
    U("have you been able to stick to the plan?", "en", "h-rv-cbti"),
    U("日记是什么时候写的？", "zh-CN", "h-rv-diary-method"),
    U("when do you fill in the diary?", "en", "h-rv-diary-method"),
    U("最近有没有吃新的药？", "zh-CN", "h-rv-meds"),
    U("have you seen another doctor since last time?", "en", "h-rv-meds"),
    U("晚上起来有没有站不稳？", "zh-CN", "h-rv-night-events"),
    U("have you been unsteady or fallen at night?", "en", "h-rv-night-events"),
    U("早上还开车吗？", "zh-CN", "h-rv-morning"),
    U("do you drive in the mornings?", "en", "h-rv-morning"),
    U("这两周心情好吗？", "zh-CN", "h-rv-mood"),
    U("any thoughts of harming yourself lately?", "en", "h-rv-mood"),
]

OUTCOME = L("复诊时权衡相互矛盾的睡眠证据（手表与日记），并对新开的催眠药与安神中药同用作核查：改自己的处方、给安全建议、当天联系开药医生，而不是自行停用他人的药或加强镇静。",
            "At review, weigh conflicting sleep evidence (a watch against a diary) and review a newly prescribed hypnotic taken with calming herbs: change your own prescription, give safety advice and contact the prescriber the same day, rather than stopping another prescriber's medicine or adding sedation.")

DEBRIEF = {
    "title": L("复盘：慢性失眠——手表与日记不一致，安眠药与安神中药同用", "Debrief: chronic insomnia — the watch and the diary disagree, and a hypnotic meets calming herbs"),
    "conclusion": L(
        "初诊同 tcm-sg-insomnia-01。复诊时手表报告每晚6小时50分、“深睡不足”，而她每天早上、看手表前写的日记是5小时20分。消费级手表常把安静的清醒算作睡眠，分期也不可靠；治疗以日记为准。为了追分数，她提早上床、晚起，睡眠效率由约90%降到约67%。她又因分数焦虑去看私人诊所，服唑吡坦10毫克，与睡前安神中药同服，夜里照顾婆婆时站不稳撞伤、早上头昏仍开车。正确做法：解释手表、恢复时间表，暂停睡前那包中药，给安全建议，当天联系开药医生，由他决定剂量与是否继续。",
        "First visit as in tcm-sg-insomnia-01. At review the watch reports 6 h 50 min a night and \"too little deep sleep\", while the diary she writes each morning before looking at the watch shows 5 h 20 min. Consumer watches often count quiet waking as sleep and stage sleep poorly; the diary is the working measure. Chasing the score, she went to bed earlier and rose later, and her sleep efficiency fell from about 90% to about 67%. Worried by the score, she saw a private GP and has taken zolpidem 10 mg with the bedtime sachet of calming herbs; getting up at night for her mother-in-law she was unsteady and hurt herself, and she drives while groggy. The right course: explain the watch, restart the schedule, hold the bedtime sachet, give safety advice, and contact the prescriber the same day — the dose and whether to continue are his decision.",
    ),
    "keyReasoning": base.DEBRIEF["keyReasoning"][:4] + [
        L("证据不一致时，先问每份证据是怎么产生的：日记每天早上、看手表前写，方法一致；手表靠动作与心率推算，不是经过失眠验证的测量。",
          "When evidence conflicts, ask how each piece was produced: the diary is written each morning before she sees the watch, the same way every day; the watch infers sleep from movement and heart rate and is not a measure validated in insomnia."),
        L("每次复诊都问“有没有新的药、看过别的医生”：她不会主动说。改自己能改的，协调别人的。",
          "Ask at every review about new medicines and other doctors: she will not volunteer them. Change what is yours; coordinate what is someone else's."),
    ],
    "teachingPoints": base.DEBRIEF["teachingPoints"][:4] + [
        L("消费级睡眠追踪器与多导睡眠图相比常高估总睡眠、低估夜间清醒，睡眠分期不可靠；过度追求分数（“正睡症”，orthosomnia）会加重失眠。",
          "Against polysomnography, consumer sleep trackers tend to overestimate total sleep and underestimate night-time waking, and stage sleep unreliably; chasing the numbers (\"orthosomnia\") can make insomnia worse."),
        L("唑吡坦：美国FDA建议女性起始剂量5毫克（次日残留作用），并就复杂睡眠行为加黑框警示；服药后需能在床上待足7–8小时。与安神中药同用可能加重镇静，直接证据有限，谨慎处理并告知开药医生。",
          "Zolpidem: the US FDA recommends a 5 mg starting dose for women (next-morning effects) and has a boxed warning about complex sleep behaviours; a dose needs 7–8 hours in bed after it. With calming herbs it may add to sedation; direct evidence is limited, so act cautiously and tell the prescriber."),
        L("朱砂为硫化汞，有蓄积毒性，不用于失眠的调理。", "Cinnabar is mercury sulphide, which accumulates; it has no place in treating insomnia."),
    ],
    "references": base.REFERENCES + [
        "de Zambotti M, Cellini N, Goldstone A, Colrain IM, Baker FC. Wearable sleep technology in clinical and research settings. Med Sci Sports Exerc. 2019;51(7):1538-57.",
        "Baron KG, Abbott S, Jao N, Manalo N, Mullen R. Orthosomnia: are some patients taking the quantified self too far? J Clin Sleep Med. 2017;13(2):351-4.",
        "Harvey AG, Tang NK. (Mis)perception of sleep in insomnia: a puzzle and a resolution. Psychol Bull. 2012;138(1):77-101.",
        "US Food and Drug Administration. FDA Drug Safety Communication: risk of next-morning impairment after use of insomnia drugs; FDA requires lower recommended doses for certain drugs containing zolpidem. Silver Spring (MD): FDA; 2013.",
        "US Food and Drug Administration. FDA adds Boxed Warning for risk of serious injuries caused by sleepwalking with certain prescription insomnia medicines. Silver Spring (MD): FDA; 2019.",
    ],
}


def build() -> dict:
    c = insomnia_family.variant(
        case_id=CASE_ID,
        version="0.1.0",
        variant_id="review-b-conflicting-evidence",
        title=L("失眠 · 47岁女性 · 复诊B", "Difficulty sleeping · 47-year-old woman · review B"),
        outcome=OUTCOME,
        review={"history": HISTORY, "exam": EXAM, "investigations": INVESTIGATIONS, "interventions": INTERVENTIONS, "decisions": DECISIONS,
                "objectives": OBJECTIVES, "rubric": RUBRIC, "safetyGates": SAFETY_GATES, "solution": SOLUTION, "utterances": UTTERANCES},
        debrief=DEBRIEF,
        tcmcraft={
            "modules": base.build()["extensions"]["tcmcraft"]["modules"] + ["evidence-quality", "herb-drug-review"],
            "unacceptable": ["defer-to-senior", "combine-formulas", "stronger-sleeper", *HARMS],
            "evidenceConflict": {
                "sources": [
                    {"id": "sleep-diary-review", "kind": "patient-reported", "method": "written each morning before looking at the watch", "sleep": "5 h 20 min"},
                    {"id": "watch-export", "kind": "consumer wearable", "method": "movement and heart rate; not a medical device", "sleep": "6 h 50 min"},
                ],
                "resolution": "diary as the working measure; watch read with caution; neither is ground truth",
            },
            "expertDisagreement": base.build()["extensions"]["tcmcraft"]["expertDisagreement"] + [
                "Whether to hold the bedtime sachet or the whole formula while she takes zolpidem (the case holds the bedtime sachet).",
            ],
            "followUpModel": "authored branch (not a calibrated outcome model)",
        },
    )
    for npc in c["npcs"]:
        if npc["role"] == "pharmacist":
            npc["interprets"] = npc["interprets"] + ["zolpidem-label"]
            npc["knowledge"] = L(
                npc["knowledge"]["zh-CN"] + "也可说明唑吡坦：次日残留作用（美国FDA建议女性起始剂量5毫克）、复杂睡眠行为的黑框警示、服药后需能在床上待足7–8小时；与安神中药同用可能加重镇静，直接证据有限。",
                npc["knowledge"]["en"] + " Can also explain zolpidem: next-morning effects (the US FDA recommends a 5 mg starting dose for women), the boxed warning about complex sleep behaviours, and the need for 7–8 hours in bed after a dose; with calming herbs it may add to sedation, though direct evidence is limited.")
        if npc["role"] == "attending":
            npc["interprets"] = npc["interprets"] + ["watch-export"]
    return c
