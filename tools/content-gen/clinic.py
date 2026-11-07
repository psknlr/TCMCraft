"""The fictional Singapore community TCM clinic: equipment catalog, room templates and facility.

Coordinates follow docs/FACILITIES.md of ClinicalCraft: 1 unit = 1 m, +Y up, an equipment origin is the centre of
its footprint on the floor, its front faces +Z at `rot: 0`, and a room template's door is on its local south (+Z).
TCM-specific semantics stay in tags (`tcm`, `acupuncture`, …): the capability vocabulary has no TCM entries yet
(docs/ENGINE_EXTENSIONS.md §1), so the equipment provides only canonical capabilities (`medications`, `records`).
"""

from __future__ import annotations

from common import L

CATALOG_ID = "tcmcraft-clinic"
FACILITY_ID = "tcm-sg-clinic"


def part(m, p, s, **extra):
    out = {"m": m, "p": [round(v, 4) for v in p], "s": [round(v, 4) for v in s]}
    out.update(extra)
    return out


MATERIALS = [
    {"id": "tcm-rosewood", "color": "#6b3424", "pattern": "plank", "variance": 0.08},
    {"id": "tcm-drawer", "color": "#a0623a", "pattern": "plank", "variance": 0.06},
    {"id": "tcm-brass", "color": "#c8a24a", "pattern": "flat", "variance": 0.04, "metalness": 0.4, "roughness": 0.45},
    {"id": "tcm-leather", "color": "#9c6b4a", "pattern": "noise", "variance": 0.05, "roughness": 0.7},
    {"id": "tcm-chart-paper", "color": "#efe2c4", "pattern": "noise", "variance": 0.04},
    {"id": "tcm-meridian", "color": "#b83a2e", "pattern": "flat", "variance": 0.02},
    {"id": "tcm-jade", "color": "#5f9e86", "pattern": "flat", "variance": 0.04},
    {"id": "tcm-warm-lamp", "color": "#f2c98a", "pattern": "flat", "variance": 0.02, "emissive": "#ffb35c", "emissiveIntensity": 0.6},
    {"id": "tcm-ring-light", "color": "#f4f7fb", "pattern": "flat", "variance": 0.01, "emissive": "#ffffff", "emissiveIntensity": 0.8},
    {"id": "tcm-tdp-plate", "color": "#c4552b", "pattern": "flat", "variance": 0.03, "emissive": "#ff6a2a", "emissiveIntensity": 0.4},
]


def herb_cabinet():
    parts = [
        part("darkwood", [0, 0.05, 0], [2.0, 0.1, 0.55]),
        part("tcm-rosewood", [0, 1.1, -0.02], [2.0, 2.0, 0.5]),
        part("darkwood", [0, 2.15, 0], [2.0, 0.1, 0.55]),
        part("tcm-meridian", [0, 2.0, 0.24], [0.8, 0.12, 0.02]),
    ]
    for row in range(5):
        y = 0.35 + row * 0.32
        for col in range(6):
            x = -0.8 + col * 0.32
            parts.append(part("tcm-drawer", [x, y, 0.24], [0.29, 0.29, 0.02]))
            parts.append(part("tcm-brass", [x, y, 0.255], [0.04, 0.04, 0.02]))
    return {
        "id": "tcm-herb-cabinet",
        "name": L("百子柜（中药饮片斗柜）", "Herb drawer cabinet (百子柜)"),
        "category": "storage",
        "description": L("传统中药斗柜：每个抽屉存放一味饮片或配方颗粒，抽屉面写药名，外观或名称相近的药材分开放置。",
                         "A traditional herb drawer cabinet: each drawer holds one medicinal (cut crude herb or granules), labelled with its name; look-alike and sound-alike herbs are kept apart."),
        "usage": L("按处方的现行版本逐味取药称量，核对药名、规格与剂量；不得自行替换。",
                   "Weigh out each medicinal against the current version of the prescription, checking name, form and dose; never substitute on your own."),
        "capabilities": ["medications"],
        "footprint": {"w": 2.0, "d": 0.55, "h": 2.2},
        "solid": True,
        "interaction": {"kind": "device", "prompt": L("E · 取药", "E · Take medicinals")},
        "screen": "none",
        "tags": ["tcm", "dispensary", "herbs", "storage"],
        "parts": parts,
    }


def granule_dispenser():
    parts = [
        part("coal", [0, 0.05, 0], [1.4, 0.1, 0.8]),
        part("white", [0, 1.05, -0.02], [1.36, 1.9, 0.74]),
        part("glass", [0, 1.45, 0.36], [1.1, 0.7, 0.02]),
        part("black", [-0.35, 0.95, 0.36], [0.36, 0.26, 0.02]),
        part("screen-dark", [-0.35, 0.95, 0.372], [0.32, 0.22, 0.004], name="screen"),
        part("steel", [0.3, 0.75, 0.33], [0.5, 0.06, 0.1]),
        part("coal", [0.3, 0.95, 0.36], [0.4, 0.06, 0.02]),
        part("led-green", [0.55, 1.88, 0.36], [0.06, 0.06, 0.02], anim="blink"),
    ]
    for i in range(6):
        parts.append(part("tcm-jade" if i % 2 == 0 else "beige", [-0.45 + i * 0.18, 1.45, 0.33], [0.12, 0.5, 0.04]))
    return {
        "id": "tcm-granule-dispenser",
        "name": L("配方颗粒自动调剂机", "Automated granule dispenser"),
        "category": "therapy",
        "description": L("按处方逐味称取单味配方颗粒、混合并分装成药包的调剂设备，记录批号与称量结果。",
                         "Weighs single-herb concentrated granules for each item on the prescription, mixes them and seals them into sachets, recording batch numbers and weights."),
        "usage": L("扫描现行版本处方后调剂；设备拒绝已作废或待处理的版本。核对药包数量与标签后发药。",
                   "Scan the current version of the prescription to start; the machine refuses a cancelled or pending version. Check the sachet count and label before supply."),
        "capabilities": ["medications"],
        "footprint": {"w": 1.4, "d": 0.8, "h": 2.0},
        "solid": True,
        "interaction": {"kind": "device", "prompt": L("E · 调剂颗粒", "E · Dispense granules")},
        "screen": "text",
        "tags": ["tcm", "dispensary", "granules"],
        "parts": parts,
    }


def decoction_machine():
    return {
        "id": "tcm-decoction-machine",
        "name": L("煎药机", "Herbal decoction machine"),
        "category": "therapy",
        "description": L("密闭煎煮并自动包装汤剂的煎药机，用于饮片处方的代煎。", "Decocts crude-herb prescriptions in a sealed pot and packs the decoction into pouches."),
        "usage": L("按处方的先煎、后下要求设定程序；记录煎煮时间与包数。", "Set the programme for any herbs to be decocted first or added late; record the time and the number of pouches."),
        "capabilities": [],
        "footprint": {"w": 0.6, "d": 0.6, "h": 1.3},
        "solid": True,
        "interaction": {"kind": "none", "prompt": L("E · 查看煎药机", "E · Check the decoction machine")},
        "screen": "none",
        "tags": ["tcm", "dispensary", "decoction"],
        "parts": [
            part("steel", [0, 0.2, 0], [0.55, 0.4, 0.55]),
            part("chrome", [0, 0.75, 0], [0.5, 0.7, 0.5]),
            part("steel", [0, 1.15, 0], [0.52, 0.1, 0.52]),
            part("coal", [0, 1.25, 0], [0.1, 0.1, 0.1]),
            part("coal", [0, 0.6, 0.27], [0.3, 0.2, 0.02]),
            part("led-red", [0.1, 0.6, 0.285], [0.04, 0.04, 0.01], anim="blink"),
            part("chrome", [0.2, 0.3, 0.27], [0.06, 0.06, 0.04]),
        ],
    }


def tongue_station():
    return {
        "id": "tcm-tongue-imaging-station",
        "name": L("舌象采集仪", "Tongue-imaging station"),
        "category": "imaging",
        "description": L("带下颌托、标准环形光源和色卡的舌象采集仪，记录拍摄时间与质量校验结果。",
                         "A tongue-imaging station with a chin rest, a standard ring light and a colour reference card; it records the capture time and a quality check."),
        "usage": L("请患者漱口、休息片刻，下颌放在托上自然伸舌；色卡入画、光源开启后拍摄，质量校验不通过即重拍。",
                   "Have the patient rinse and settle, rest the chin and put the tongue out naturally; capture with the colour card in frame and the ring light on, and repeat if the quality check fails."),
        "capabilities": [],
        "footprint": {"w": 0.7, "d": 0.6, "h": 1.5},
        "solid": True,
        "interaction": {"kind": "none", "prompt": L("E · 舌象采集仪", "E · Tongue-imaging station")},
        "screen": "text",
        "tags": ["tcm", "inspection", "tongue", "imaging"],
        "parts": [
            part("coal", [0, 0.03, 0], [0.6, 0.06, 0.5]),
            part("steel", [0, 0.6, -0.15], [0.08, 1.1, 0.08]),
            part("white", [0, 1.25, -0.1], [0.5, 0.4, 0.3]),
            part("tcm-ring-light", [0, 1.25, 0.06], [0.3, 0.3, 0.02]),
            part("black", [0, 1.25, 0.075], [0.1, 0.1, 0.01]),
            part("steel", [0, 1.02, 0.08], [0.04, 0.04, 0.12]),
            part("plastic", [0, 1.0, 0.2], [0.3, 0.04, 0.15]),
            part("paper", [-0.2, 1.08, 0.18], [0.09, 0.06, 0.005]),
            part("red", [-0.23, 1.08, 0.184], [0.02, 0.04, 0.002]),
            part("green", [-0.2, 1.08, 0.184], [0.02, 0.04, 0.002]),
            part("blue", [-0.17, 1.08, 0.184], [0.02, 0.04, 0.002]),
            part("black", [0.3, 1.2, -0.1], [0.08, 0.3, 0.25]),
            part("screen-dark", [0.343, 1.2, -0.1], [0.004, 0.26, 0.21], name="screen"),
        ],
    }


def intake_kiosk():
    return {
        "id": "tcm-intake-kiosk",
        "name": L("自助问诊机（含舌象拍照）", "Self-service intake kiosk (with tongue photo)"),
        "category": "computing",
        "description": L("候诊区的自助问诊机：填写问卷并用顶部摄像头自拍舌象。照明为环境暖光，没有固定色卡。",
                         "A waiting-area kiosk: patients fill in a questionnaire and photograph their own tongue with the camera on top. It relies on the room's warm lighting and has no fixed colour card."),
        "usage": L("自助机照片只作参考；颜色校验未通过时提示重拍，临床判断以诊室内的望舌或标准采集为准。",
                   "Kiosk photos are for reference only; it flags a failed colour check, and clinical judgement rests on inspection in the consulting room or a standard capture."),
        "capabilities": [],
        "footprint": {"w": 0.6, "d": 0.5, "h": 1.6},
        "solid": True,
        "interaction": {"kind": "none", "prompt": L("E · 自助问诊机", "E · Intake kiosk")},
        "screen": "text",
        "tags": ["tcm", "intake", "kiosk", "waiting"],
        "parts": [
            part("coal", [0, 0.03, 0], [0.5, 0.06, 0.4]),
            part("white", [0, 0.6, 0], [0.12, 1.1, 0.12]),
            part("white", [0, 1.35, 0], [0.55, 0.5, 0.12]),
            part("black", [0, 1.33, 0.065], [0.48, 0.36, 0.01]),
            part("screen-dark", [0, 1.33, 0.072], [0.44, 0.32, 0.004], name="screen"),
            part("tcm-warm-lamp", [0, 1.56, 0.065], [0.16, 0.04, 0.01]),
            part("black", [0, 1.56, 0.071], [0.03, 0.03, 0.004]),
            part("teal", [0, 0.9, 0.065], [0.12, 0.2, 0.01]),
        ],
    }


def acupuncture_cart():
    parts = [part("rubber", [x, 0.04, z], [0.08, 0.08, 0.08]) for x in (-0.27, 0.27) for z in (-0.18, 0.18)]
    parts += [part("chrome", [x, 0.5, z], [0.03, 0.8, 0.03]) for x in (-0.3, 0.3) for z in (-0.2, 0.2)]
    parts += [
        part("steel", [0, 0.2, 0], [0.62, 0.03, 0.42]),
        part("mint", [0, 0.26, 0], [0.4, 0.08, 0.3]),
        part("steel", [0, 0.55, 0], [0.62, 0.03, 0.42]),
        part("steel", [0, 0.88, 0], [0.66, 0.04, 0.46]),
        part("white", [-0.18, 0.93, -0.1], [0.16, 0.06, 0.1]),
        part("blue", [0.0, 0.93, -0.1], [0.16, 0.06, 0.1]),
        part("lead-glass", [0.15, 0.95, 0.1], [0.1, 0.1, 0.1]),
        part("paper", [0.0, 0.94, 0.12], [0.1, 0.08, 0.1]),
        part("steel", [-0.17, 0.91, 0.12], [0.2, 0.02, 0.1]),
        part("yellow", [0.22, 0.98, -0.1], [0.14, 0.16, 0.14]),
        part("biohazard", [0.22, 1.075, -0.1], [0.15, 0.03, 0.15]),
        part("chrome", [0.34, 0.8, 0], [0.02, 0.03, 0.3]),
    ]
    return {
        "id": "tcm-acupuncture-cart",
        "name": L("针灸治疗车", "Acupuncture cart"),
        "category": "therapy",
        "description": L("针灸治疗车：一次性无菌针（多种规格）、酒精棉片、无菌棉球、弯盘、手消毒液和锐器盒。",
                         "Acupuncture cart: single-use sterile needles in several sizes, alcohol swabs, sterile cotton balls, a kidney dish, hand rub and a sharps bin."),
        "usage": L("推到治疗床旁；手卫生后取针，进针前核对针数，出针后把每一支针投入锐器盒并与进针数核对。",
                   "Wheel it to the couch; take needles after hand hygiene, note the number inserted, and on withdrawal drop every needle into the sharps bin and check the count against what went in."),
        "capabilities": [],
        "footprint": {"w": 0.7, "d": 0.5, "h": 1.1},
        "solid": True,
        "interaction": {"kind": "storage", "prompt": L("E · 取针具", "E · Take needles")},
        "screen": "none",
        "tags": ["tcm", "acupuncture", "sharps", "bedside"],
        "portable": "cart",
        "parts": parts,
    }


def acupuncture_couch():
    parts = [part("wood", [x, 0.3, z], [0.07, 0.6, 0.07]) for x in (-0.3, 0.3) for z in (-0.85, 0.85)]
    parts += [
        part("darkwood", [0, 0.15, 0], [0.6, 0.03, 1.6]),
        part("mint", [0, 0.2, 0.5], [0.4, 0.06, 0.3]),
        part("wood", [0, 0.62, 0], [0.72, 0.06, 1.9]),
        part("tcm-leather", [0, 0.69, 0], [0.72, 0.08, 1.9], name="mattress"),
        part("coal", [0, 0.732, -0.78], [0.14, 0.004, 0.1]),
        part("paper", [0, 0.733, 0.1], [0.5, 0.004, 1.4]),
    ]
    return {
        "id": "tcm-acupuncture-couch",
        "name": L("针灸推拿床（带面孔）", "Acupuncture and tuina couch (with face hole)"),
        "category": "furniture",
        "description": L("木架皮面治疗床，头端有面孔，便于俯卧针刺与推拿；铺一次性床单。",
                         "A wooden-framed, leather-topped treatment couch with a face hole at the head end for prone needling and tuina, covered with a disposable sheet."),
        "usage": L("有晕针史或紧张的患者取卧位；俯卧时腹下垫枕，面部放入面孔。", "Lie down patients who are anxious or have fainted with needles before; when prone, put a pillow under the abdomen and the face in the face hole."),
        "capabilities": [],
        "footprint": {"w": 0.75, "d": 1.95, "h": 0.75},
        "solid": True,
        "interaction": {"kind": "bed", "prompt": L("E · 治疗床", "E · Treatment couch")},
        "screen": "none",
        "tags": ["tcm", "acupuncture", "tuina", "bed", "patient-support"],
        "parts": parts,
    }


def tdp_lamp():
    return {
        "id": "tcm-tdp-lamp",
        "name": L("TDP治疗灯（神灯）", "TDP heat lamp"),
        "category": "therapy",
        "description": L("落地式TDP治疗灯，用于针刺或推拿时局部温热。", "A floor-standing TDP heat lamp for local warmth during needling or tuina."),
        "usage": L("灯头距皮肤约30–40 cm，询问患者感觉，避免烫伤；感觉减退者慎用。", "Keep the head about 30–40 cm from the skin and ask how it feels to avoid burns; take care where sensation is reduced."),
        "capabilities": [],
        "footprint": {"w": 0.6, "d": 0.6, "h": 1.7},
        "solid": True,
        "interaction": {"kind": "none", "prompt": L("E · TDP灯", "E · TDP lamp")},
        "screen": "none",
        "tags": ["tcm", "heat", "therapy"],
        "parts": [
            part("coal", [0, 0.04, 0], [0.55, 0.08, 0.55]),
            part("chrome", [0, 0.7, -0.15], [0.05, 1.25, 0.05]),
            part("chrome", [0, 1.35, -0.02], [0.05, 0.05, 0.3]),
            part("steel", [0, 1.45, 0.15], [0.3, 0.15, 0.3]),
            part("tcm-tdp-plate", [0, 1.37, 0.15], [0.26, 0.02, 0.26]),
            part("plastic", [0, 0.9, -0.1], [0.12, 0.12, 0.06]),
            part("led-amber", [0, 0.93, -0.068], [0.03, 0.03, 0.004]),
        ],
    }


def acupoint_chart():
    return {
        "id": "tcm-acupoint-chart",
        "name": L("经络穴位挂图", "Meridian and acupoint chart"),
        "category": "teaching",
        "description": L("壁挂的人体经络穴位图（背面观），标出足太阳膀胱经与常用腰背部穴位。",
                         "A wall chart of the channels and acupoints (posterior view), showing the bladder channel and the common points of the lower back."),
        "capabilities": [],
        "footprint": {"w": 1.0, "d": 0.08, "h": 2.0},
        "solid": False,
        "interaction": {"kind": "none", "prompt": L("E · 查看穴位图", "E · Read the acupoint chart")},
        "screen": "none",
        "tags": ["tcm", "wall", "teaching"],
        "parts": [
            part("darkwood", [0, 1.45, -0.03], [0.9, 1.1, 0.02]),
            part("tcm-chart-paper", [0, 1.45, -0.018], [0.84, 1.04, 0.004]),
            part("skin", [0, 1.45, -0.014], [0.18, 0.8, 0.004]),
            part("skin", [0, 1.88, -0.014], [0.1, 0.1, 0.004]),
            part("tcm-meridian", [-0.03, 1.4, -0.011], [0.008, 0.7, 0.002]),
            part("tcm-meridian", [0.03, 1.4, -0.011], [0.008, 0.7, 0.002]),
            part("blue", [-0.03, 1.25, -0.009], [0.02, 0.02, 0.002]),
            part("blue", [0.03, 1.25, -0.009], [0.02, 0.02, 0.002]),
            part("blue", [-0.03, 1.15, -0.009], [0.02, 0.02, 0.002]),
            part("blue", [0.03, 1.15, -0.009], [0.02, 0.02, 0.002]),
        ],
    }


def pulse_pillow():
    return {
        "id": "tcm-pulse-pillow",
        "name": L("脉枕", "Pulse pillow"),
        "category": "decor",
        "description": L("切脉时垫在患者腕下的小枕。", "A small cushion placed under the patient's wrist for pulse taking."),
        "usage": L("让患者手臂平放、掌心向上，腕下垫脉枕，静坐片刻后再切脉。", "Lay the arm flat, palm up, with the pillow under the wrist, and let the patient settle for a moment before taking the pulse."),
        "capabilities": [],
        "footprint": {"w": 0.22, "d": 0.12, "h": 0.08},
        "solid": False,
        "interaction": {"kind": "none"},
        "screen": "none",
        "tags": ["tcm", "palpation", "pulse"],
        "portable": "handheld",
        "parts": [
            part("navy", [0, 0.035, 0], [0.2, 0.07, 0.1]),
            part("white", [0, 0.072, 0], [0.18, 0.004, 0.08]),
        ],
    }


def catalog() -> dict:
    return {
        "schema": "clinicalcraft/equipment-catalog@1",
        "id": CATALOG_ID,
        "name": L("TCMCraft 中医诊所设备", "TCMCraft TCM clinic equipment"),
        "materials": MATERIALS,
        "equipment": [herb_cabinet(), granule_dispenser(), decoction_machine(), tongue_station(), intake_kiosk(),
                      acupuncture_cart(), acupuncture_couch(), tdp_lamp(), acupoint_chart(), pulse_pillow()],
    }


# ---------------------------------------------------------------------------------------------
# Room templates
# ---------------------------------------------------------------------------------------------

def P(id, type, x, z, rot=0, label=None, **extra):
    out = {"id": id, "type": type, "x": x, "z": z}
    if rot:
        out["rot"] = rot
    if label:
        out["label"] = label
    out.update(extra)
    return out


def consult_room() -> dict:
    return {
        "schema": "clinicalcraft/room-template@1",
        "id": "tcm-consult-room",
        "name": L("中医诊室", "TCM consulting room"),
        "description": L("中医诊室：医生诊桌与脉枕、患者座椅、舌象采集仪、诊查床、病历终端、病例讨论板和洗手池。",
                         "A TCM consulting room: the physician's desk with a pulse pillow, the patient's chair, a tongue-imaging station, an examination couch, a records terminal, a case board and a sink."),
        "kind": "consult",
        "size": {"w": 6, "d": 8},
        "floor": "floor",
        "partitions": [
            {"side": "n"},
            {"side": "w"},
            {"side": "e"},
            {"side": "s", "openings": [{"kind": "door", "width": 1.6, "height": 2.6, "offset": 1.6}]},
        ],
        "sign": {"text": L("中医诊室", "TCM consulting room"), "side": "n", "color": "#8b2e2e"},
        "lights": [{"x": 0, "z": -1.5}, {"x": 0, "z": 2}],
        "placements": [
            P("desk", "desk", 2.475, -1.5, 270, L("医生诊桌", "Physician's desk")),
            P("doctor-chair", "office-chair", 1.4, -1.5, 90),
            P("patient-chair", "chair", 2.45, -0.25, 180, L("患者座椅", "Patient's chair")),
            P("pulse-pillow", "tcm-pulse-pillow", 2.45, -0.95, 0, L("脉枕", "Pulse pillow"), y=0.76),
            P("tongue-station", "tcm-tongue-imaging-station", -2.4, -3.3, 0, L("舌象采集仪", "Tongue-imaging station")),
            P("couch", "treatment-plinth", -2.45, -1.6, 0, L("诊查床", "Examination couch")),
            P("records", "records-terminal", 2.525, 1.3, 270, L("病历终端", "Records terminal")),
            P("chart", "tcm-acupoint-chart", 0.4, -3.785, 0, L("经络穴位挂图", "Acupoint chart")),
            P("board", "evidence-board", -2.525, 1.9, 90, L("病例讨论板", "Case board")),
            P("sink", "sink", -1.2, 3.55, 180),
        ],
        "patientSlots": [
            {"id": "slot", "x": -2.3, "z": -1.6, "rot": 90, "posture": "sitting", "bed": "couch", "accepts": ["outpatient"]},
        ],
        "capabilities": ["records", "evidence-board"],
        "tags": ["tcm", "outpatient", "consult"],
    }


def treatment_room() -> dict:
    return {
        "schema": "clinicalcraft/room-template@1",
        "id": "tcm-treatment-room",
        "name": L("针灸推拿治疗室", "Acupuncture and tuina room"),
        "description": L("两张带面孔的针灸推拿床，以隔帘分隔；针灸治疗车、TDP灯、锐器盒、针数登记板、手套和洗手池。",
                         "Two acupuncture and tuina couches with face holes, separated by a curtain; an acupuncture cart, TDP lamps, a sharps bin, a needle-count board, gloves and a sink."),
        "kind": "rehabilitation",
        "size": {"w": 10, "d": 8},
        "floor": "floor",
        "partitions": [
            {"side": "n"},
            {"side": "w"},
            {"side": "e"},
            {"side": "s", "openings": [{"kind": "door", "width": 1.8, "height": 2.6, "offset": 0}]},
        ],
        "sign": {"text": L("针灸推拿治疗室", "Acupuncture & tuina"), "side": "n", "color": "#8b2e2e"},
        "lights": [{"x": -2.8, "z": -2}, {"x": 1.2, "z": -2}, {"x": 0, "z": 2}],
        "placements": [
            P("couch-1", "tcm-acupuncture-couch", -2.8, -2.4, 0, L("治疗床 1", "Couch 1")),
            P("couch-2", "tcm-acupuncture-couch", 1.2, -2.4, 0, L("治疗床 2", "Couch 2")),
            P("curtain", "privacy-curtain", -0.8, -2.6, 90),
            P("cart", "tcm-acupuncture-cart", -1.7, -1.0, 0, L("针灸治疗车", "Acupuncture cart")),
            P("lamp-1", "tcm-tdp-lamp", -4.2, -2.4, 90),
            P("lamp-2", "tcm-tdp-lamp", 2.3, -2.4, 270),
            P("sharps", "sharps-bin", -1.7, -3.4, 0, L("锐器盒", "Sharps bin")),
            P("stool-1", "stool", -1.9, -2.0),
            P("stool-2", "stool", 2.1, -1.4),
            P("gloves", "glove-dispenser", 0.0, -3.765),
            P("linen", "cabinet", 4.4, -3.0, 270, L("床单柜", "Linen cabinet")),
            P("count-board", "whiteboard", 4.765, 1.0, 270, L("针数登记板", "Needle-count board")),
            P("chart", "tcm-acupoint-chart", -4.785, 1.5, 90, L("经络穴位挂图", "Acupoint chart")),
            P("sanitizer", "hand-sanitizer", -4.5, 3.4),
            P("sink", "sink", 3.8, 3.55, 180),
        ],
        "patientSlots": [
            {"id": "slot-1", "x": -2.8, "z": -2.4, "rot": 0, "posture": "lying", "bed": "couch-1", "accepts": ["outpatient"]},
            {"id": "slot-2", "x": 1.2, "z": -2.4, "rot": 0, "posture": "lying", "bed": "couch-2", "accepts": ["outpatient"]},
        ],
        "staff": [
            {"id": "assistant", "role": "nurse", "name": L("Siti（诊所助理）", "Siti (clinic assistant)"), "x": 0.0, "z": 0.6, "rot": 180,
             "greeting": L("治疗床和治疗车都准备好了。需要帮忙让病人躺好吗？", "The couches and the cart are ready. Shall I help the patient settle on the couch?")},
        ],
        "capabilities": [],
        "tags": ["tcm", "acupuncture", "tuina", "treatment"],
    }


def dispensary() -> dict:
    return {
        "schema": "clinicalcraft/room-template@1",
        "id": "tcm-dispensary",
        "name": L("中药房", "Herbal dispensary"),
        "description": L("中药房：前部为发药窗口与中成药货架（公众区），柜台后为调剂区（仅限药房人员与护士）——百子柜、配方颗粒调剂机、煎药机、调剂台和审方终端。",
                         "The herbal dispensary: a collection counter and a shelf of Chinese proprietary medicines at the front (public area); behind the counter the dispensing area (dispensary staff and nurses only) with herb drawer cabinets, the granule dispenser, decoction machines, a dispensing bench and the prescription-review terminal."),
        "kind": "pharmacy",
        "size": {"w": 10, "d": 8},
        "floor": "tile-white",
        "partitions": [
            {"side": "n"},
            {"side": "w"},
            {"side": "e"},
            {"side": "s", "openings": [{"kind": "door", "width": 1.6, "height": 2.6, "offset": -1.5}]},
        ],
        "sign": {"text": L("中药房 · 取药", "Herbal dispensary · Collection"), "side": "n", "color": "#5f9e6e"},
        "lights": [{"x": -2, "z": -2}, {"x": 2, "z": -2}, {"x": 0, "z": 2.5}],
        "placements": [
            P("cabinet-1", "tcm-herb-cabinet", -3.0, -3.55, 0, L("百子柜 1", "Herb cabinet 1")),
            P("cabinet-2", "tcm-herb-cabinet", -0.8, -3.55, 0, L("百子柜 2", "Herb cabinet 2")),
            P("cabinet-3", "tcm-herb-cabinet", 1.4, -3.55, 0, L("百子柜 3", "Herb cabinet 3")),
            P("granules", "tcm-granule-dispenser", 3.9, -3.425, 0, L("配方颗粒调剂机", "Granule dispenser")),
            P("decoction-1", "tcm-decoction-machine", 4.5, -1.6, 270, L("煎药机 1", "Decoction machine 1")),
            P("decoction-2", "tcm-decoction-machine", 4.5, -0.8, 270, L("煎药机 2", "Decoction machine 2")),
            P("bench", "desk", 0.0, -1.6, 0, L("调剂台", "Dispensing bench")),
            P("review-terminal", "records-terminal", -4.4, -1.0, 90, L("审方终端", "Prescription-review terminal")),
            P("counter", "reception-desk", -1.5, 1.0, 180, L("发药窗口", "Collection counter")),
            P("cpm-shelf", "pharmacy-shelves", -4.575, 2.5, 90, L("中成药货架", "Chinese proprietary medicines")),
            P("waiting", "waiting-chairs", 2.5, 3.4, 180),
        ],
        "staff": [
            {"id": "dispenser", "role": "pharmacist", "name": L("林先生（中药调剂）", "Mr Lim (TCM dispensing)"), "x": -1.5, "z": -0.2, "rot": 0,
             "greeting": L("处方开好了吗？我按现行版本审方和调剂，有问题会马上告诉你。", "Prescription ready? I review and fill the current version, and I'll tell you straight away if anything needs sorting.")},
        ],
        "zones": [
            {"id": "dispensing", "name": L("中药调剂区", "Dispensing area"), "rect": {"x": 0, "z": -1.75, "w": 10, "d": 4.5}, "roles": ["pharmacist", "nurse"]},
        ],
        "capabilities": ["medications", "records"],
        "tags": ["tcm", "dispensary", "pharmacy", "restricted"],
    }


def templates() -> list[dict]:
    return [consult_room(), treatment_room(), dispensary()]


# ---------------------------------------------------------------------------------------------
# Facility
# ---------------------------------------------------------------------------------------------

def facility() -> dict:
    return {
        "schema": "clinicalcraft/facility@1",
        "id": FACILITY_ID,
        "name": L("TCMCraft 社区中医诊所（虚构，新加坡）", "TCMCraft Community TCM Clinic (fictional, Singapore)"),
        "description": L(
            "虚构的新加坡社区中医诊所，一层：入口候诊大厅（挂号台、自助问诊机）、三间中医诊室（含一间复诊与远程会诊室）、针灸推拿治疗室、中药房（发药窗口与限制进入的调剂区）和物品库房。附近有巴士站。",
            "A fictional single-storey community TCM clinic in Singapore: an entrance waiting hall (registration and an intake kiosk), three TCM consulting rooms (one used for reviews and teleconsultation), an acupuncture and tuina room, the herbal dispensary (a collection counter and a restricted dispensing area) and a store. A bus stop is close by.",
        ),
        "bounds": {"minX": -30, "maxX": 30, "minZ": -20, "maxZ": 28},
        "spawn": {"x": -5, "z": 20, "yaw": 0},
        "environment": {"sky": "#9fc9d9", "fog": {"color": "#c3d8d6", "near": 40, "far": 90}, "sunIntensity": 3.2},
        "catalogs": ["materials", "core-furniture", "core-clinical", "core-diagnostics", CATALOG_ID],
        "terrain": {
            "ground": "grass",
            "paths": [
                {"x": -5, "z": 13, "w": 10, "d": 6, "material": "stone"},
                {"x": -5, "z": 21, "w": 3, "d": 10, "material": "path"},
                {"x": 0, "z": 25, "w": 50, "d": 3, "material": "asphalt"},
            ],
            "trees": [
                {"x": -22, "z": -14, "h": 7}, {"x": -10, "z": -15, "h": 6}, {"x": 4, "z": -15, "h": 7}, {"x": 18, "z": -14, "h": 6},
                {"x": -22, "z": 4, "h": 8}, {"x": 22, "z": 2, "h": 7}, {"x": -16, "z": 16, "h": 6}, {"x": 8, "z": 16, "h": 7},
                {"x": 20, "z": 14, "h": 8}, {"x": -26, "z": 20, "h": 6},
            ],
            "flowers": {"count": 40, "seed": 6502, "exclude": [{"x": 0, "z": 0, "w": 34, "d": 22}, {"x": -5, "z": 17, "w": 10, "d": 14}, {"x": 0, "z": 25, "w": 52, "d": 4}]},
            "horizon": {"count": 36, "radius": 52},
            "clouds": 16,
        },
        "buildings": [
            {
                "id": "clinic",
                "name": L("TCMCraft 社区中医诊所", "TCMCraft Community TCM Clinic"),
                "rect": {"x": 0, "z": 0, "w": 32, "d": 20},
                "floor": "floor",
                "walls": {"height": 4.5, "base": "teal", "body": "cream", "top": "wood", "thickness": 0.35},
                "openings": [
                    {"side": "s", "offset": -5, "width": 3, "height": 3, "kind": "double-door"},
                    {"side": "s", "offset": -12, "width": 3, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "s", "offset": 1, "width": 3, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "n", "offset": -13, "width": 2, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "n", "offset": -7, "width": 2, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "n", "offset": 1, "width": 3, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "n", "offset": 9, "width": 2, "height": 1.6, "sill": 1.0, "kind": "window"},
                    {"side": "w", "offset": 6, "width": 3, "height": 1.6, "sill": 1.0, "kind": "window"},
                ],
                "roof": {"material": "roof"},
                "sign": {"text": L("TCMCraft 社区中医诊所", "TCMCraft Community TCM Clinic"), "side": "s", "color": "#8b2e2e"},
            }
        ],
        "rooms": [
            {"id": "corridor", "name": L("诊所走廊", "Clinic corridor"), "kind": "corridor", "building": "clinic",
             "rect": {"x": 0, "z": 0, "w": 32, "d": 4}, "floor": "lino",
             "lights": [{"x": -12, "z": 0}, {"x": -4, "z": 0}, {"x": 4, "z": 0}, {"x": 12, "z": 0}]},
            {"id": "lobby", "name": L("候诊大厅", "Waiting hall"), "kind": "reception", "building": "clinic",
             "rect": {"x": -5, "z": 6, "w": 22, "d": 8}, "floor": "stone",
             "sign": {"text": L("挂号 · 候诊", "Registration · Waiting"), "side": "n", "color": "#8b2e2e"},
             "lights": [{"x": -12, "z": 6}, {"x": -5, "z": 6}, {"x": 2, "z": 6}]},
            {"id": "store", "name": L("物品库房", "Store"), "kind": "storage", "building": "clinic",
             "rect": {"x": 14, "z": -6, "w": 4, "d": 8}, "floor": "lino",
             "partitions": [{"side": "s", "openings": [{"kind": "door", "width": 1.4, "height": 2.6, "offset": 0}]}],
             "lights": [{"x": 14, "z": -6}]},
        ],
        "placements": [
            P("reception-desk", "reception-desk", -12, 6.0, 0, L("挂号台", "Registration"), room="lobby"),
            P("kiosk", "tcm-intake-kiosk", 2.5, 3.0, 0, L("自助问诊机（舌象拍照）", "Intake kiosk (tongue photo)"), room="lobby"),
            P("waiting-1", "waiting-chairs", -9.6, 5.2, 0, room="lobby"),
            P("waiting-2", "waiting-chairs", -7.6, 5.2, 0, room="lobby"),
            P("waiting-3", "waiting-chairs", -2.4, 5.2, 0, room="lobby"),
            P("waiting-4", "waiting-chairs", -0.4, 5.2, 0, room="lobby"),
            P("waiting-5", "waiting-chairs", -2.4, 7.0, 0, room="lobby"),
            P("waiting-6", "waiting-chairs", -0.4, 7.0, 0, room="lobby"),
            P("water", "water-dispenser", 4.5, 8.8, 0, room="lobby"),
            P("plant-1", "potted-plant", -15.2, 9.2, 0, room="lobby"),
            P("plant-2", "potted-plant", 5.2, 9.2, 0, room="lobby"),
            P("sanitizer", "hand-sanitizer", -3.2, 9.4, 0, room="lobby"),
            P("store-cabinet-1", "cabinet", 15.4, -8.5, 270, room="store"),
            P("store-cabinet-2", "cabinet", 15.4, -7.2, 270, room="store"),
            P("store-locker", "locker", 15.4, -5.6, 270, room="store"),
            P("store-bin", "trash-bin", 12.8, -9.2, 0, room="store"),
            P("bus-stop", "bus-stop", 8, 22.5, 0),
            P("bench", "garden-bench", -12, 15, 0),
            P("lamp-1", "lamp-post", -8, 12, 0),
            P("lamp-2", "lamp-post", -2, 12, 0),
        ],
        "patientSlots": [],
        "staff": [
            {"id": "receptionist", "role": "receptionist", "name": L("前台", "Reception"), "room": "lobby", "x": -12, "z": 4.9, "rot": 180,
             "greeting": L("您好！请先在自助机填问卷、拍舌象，然后在这里挂号。华语、英语都可以。", "Hello! Please fill in the questionnaire and take the tongue photo at the kiosk, then register here. Mandarin or English is fine.")},
            {"id": "senior-physician", "role": "attending", "name": L("何医生（资深中医师）", "Dr Ho (senior TCM physician)"), "room": "consult-3", "x": 8.0, "z": -4.5, "rot": 180,
             "greeting": L("有病例想讨论？先说说你掌握了哪些证据，各自可靠到什么程度。", "Want to talk a case through? Start with the evidence you have and how far each piece can be trusted.")},
        ],
        "signs": [
            {"text": L("中医诊所 · 入口", "TCM clinic · Entrance"), "x": -7.5, "y": 2.4, "z": 14.5, "rot": 0, "width": 2.6, "color": "#8b2e2e", "post": True},
        ],
        "outdoorRegion": L("诊所外", "Outside the clinic"),
        "instances": [
            {"id": "consult-1", "template": "tcm-consult-room", "x": -13, "z": -6,
             "overrides": {"name": L("中医诊室 1", "TCM consulting room 1"), "sign": {"text": L("诊室 1", "Room 1"), "side": "n", "color": "#8b2e2e"}}},
            {"id": "consult-2", "template": "tcm-consult-room", "x": -7, "z": -6,
             "overrides": {"name": L("中医诊室 2", "TCM consulting room 2"), "sign": {"text": L("诊室 2", "Room 2"), "side": "n", "color": "#8b2e2e"}}},
            {"id": "treatment", "template": "tcm-treatment-room", "x": 1, "z": -6},
            {"id": "consult-3", "template": "tcm-consult-room", "x": 9, "z": -6,
             "overrides": {"name": L("复诊与远程会诊室", "Review and teleconsultation room"), "sign": {"text": L("复诊 · 远程会诊", "Review · Teleconsultation"), "side": "n", "color": "#8b2e2e"}}},
            {"id": "dispensary", "template": "tcm-dispensary", "x": 11, "z": 6, "rot": 180},
        ],
    }
