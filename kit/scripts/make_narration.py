# -*- coding: utf-8 -*-
"""코드 한줄한줄 해설 — 씬(세그먼트) 단위 TTS 생성 + 타이밍 실측 + 병합"""
import asyncio, json, subprocess, os

VOICE = "ko-KR-InJoonNeural"
RATE = "+4%"
SEG_GAP = 0.35   # 같은 씬 안 세그먼트 사이
SCENE_GAP = 0.7  # 씬 사이
LEAD = 0.6

# (scene_id, [seg texts], extra_after_seconds)
SCENES = [
    ("s01", ["통합과학 2, 변화와 다양성 단원입니다. 오늘은 화학 변화의 첫 번째 이야기, 산화와 환원을 공부하겠습니다. 산소가 오가고, 전자가 오가는 반응이 우리 생활과 인류의 역사를 어떻게 바꿔 왔는지 함께 살펴볼까요?"], 0),
    ("s02", [
        "먼저 산소의 이동으로 산화와 환원을 정의해 봅시다. 산화는 물질이 산소를 얻는 반응이고, 환원은 물질이 산소를 잃는 반응입니다.",
        "그런데 중요한 건, 이 둘이 항상 동시에 일어난다는 점입니다. 한 물질이 산소를 잃고 환원되면, 다른 물질이 그 산소를 얻어 산화되니까요. 이것을 산화 환원 반응의 동시성이라고 합니다.",
    ], 0),
    ("s03", [
        "산화 환원 반응은 자연과 인류의 역사에 큰 변화를 가져왔습니다. 첫째, 광합성. 식물은 엽록체에서 빛 에너지를 이용해 물과 이산화 탄소로부터 포도당과 산소를 만듭니다. 이때 이산화 탄소는 환원되고, 물은 산화됩니다.",
        "둘째, 화석 연료의 연소. 화석 연료가 타면 이산화 탄소와 물이 생기면서 많은 에너지가 나옵니다. 메테인의 연소에서 메테인은 산화되고, 산소는 환원되지요. 이 에너지를 산업과 교통에 쓰면서 인류의 삶은 풍요로워졌습니다.",
        "셋째, 철의 제련. 산화 철이 주성분인 철광석에서 순수한 철을 얻는 과정입니다. 산화 철 삼과 일산화 탄소가 반응하면, 산화 철은 환원되고 일산화 탄소는 산화됩니다. 이렇게 얻은 철로 기구와 건축물을 만들었습니다.",
    ], 0),
    ("s04", [
        "실험으로 확인해 볼까요? 검은색 산화 구리 이와 탄소 가루를 섞어 시험관에 넣고 충분히 가열하면, 석회수가 뿌옇게 흐려지면서 시험관 속에 붉은색 물질이 생깁니다. 석회수가 흐려진 건 이산화 탄소 기체가 나왔기 때문이고, 붉은색 물질은 구리입니다.",
        "정리하면, 검은색 산화 구리는 산소를 잃고 붉은색 구리로 환원되고, 동시에 탄소는 산소를 얻어 이산화 탄소로 산화된 것입니다.",
        "구리판 가열 실험도 같은 원리예요. 구리판을 알코올램프 겉불꽃에 넣으면 산소를 얻어 검은 산화 구리로 산화되고, 질량은 늘어납니다. 검게 변한 구리판을 속불꽃에 넣으면, 불완전 연소로 생긴 일산화 탄소 때문에 산소를 잃고 다시 붉은 구리로 환원되며 질량은 줄어듭니다.",
    ], 0),
    ("s05", [
        "이제 한 단계 더 들어가서, 전자의 이동으로 산화와 환원을 정의해 봅시다. 산화는 물질이 전자를 잃는 반응, 환원은 물질이 전자를 얻는 반응입니다. 역시 동시에 일어납니다.",
        "그리고 산화로 잃은 전자 수와 환원으로 얻은 전자 수는 항상 같습니다. 예를 들어 아연은 전자를 두 개 잃고 산화되어 아연 이온이 되고, 구리 이온은 그 전자 두 개를 얻어 환원되어 구리가 됩니다.",
    ], 0),
    ("s06", [
        "금속과 금속 염 수용액의 반응을 봅시다. 황산 구리 이 수용액에 아연을 넣으면, 반응성이 큰 아연이 전자를 잃고 산화되어 양이온이 되고, 수용액 속 구리 이온은 전자를 얻어 환원되어 금속 구리로 석출됩니다. 그래서 수용액의 푸른색은 점점 옅어집니다.",
        "이때 아연 이온 한 개가 생길 때 구리 이온 한 개가 사라지므로, 수용액 속 전체 이온 수는 일정합니다. 반응성은 아연이 구리보다 크다는 것도 알 수 있지요.",
        "반대로 질산 은 수용액에 구리를 넣으면, 구리가 산화되어 구리 이온이 되고 은 이온이 환원되어 은으로 석출됩니다. 수용액은 푸른색이 진해지고, 구리 이온 한 개가 생길 때 은 이온 두 개가 줄어드니 전체 이온 수는 감소합니다.",
    ], 0),
    ("s07", [
        "금속과 묽은 염산의 반응도 산화 환원입니다. 마그네슘을 묽은 염산에 넣으면 마그네슘은 전자를 잃고 산화되어 마그네슘 이온이 되고, 수소 이온이 전자를 얻어 환원되면서 수소 기체가 발생합니다. 이런 반응은 금속이 수소보다 반응성이 클 때만 일어나요. 마그네슘과 아연은 반응하지만, 구리와 은은 반응하지 않습니다.",
        "금속과 비금속도 직접 반응할 수 있습니다. 나트륨과 염소, 마그네슘과 산소처럼요. 금속은 전자를 잃고 양이온이, 비금속은 전자를 얻고 음이온이 되어 이온 결합을 만듭니다.",
        "결국 산소가 이동하는 반응도 전자의 이동으로 설명됩니다. 산소를 얻는 산화는 전자를 잃는 것이고, 산소를 잃는 환원은 전자를 얻는 것입니다. 마그네슘이 타서 산화 마그네슘이 될 때, 마그네슘은 전자를 잃고 산소는 그 전자를 얻는 거죠.",
    ], 0),
    ("s08", [
        "일상생활 속에도 산화 환원 반응이 가득합니다. 깎아 둔 사과가 갈색으로 변하는 갈변, 반딧불이 몸속 루시페린이 산화될 때 나는 빛, 철가루가 산화되며 열을 내는 일회용 손난로.",
        "화약이 산화되며 높은 열을 내는 불꽃놀이, 과산화 수소가 멜라닌 색소를 산화시키는 머리카락 염색, 그리고 누렇게 변한 옷을 하얗게 만드는 섬유 표백까지. 모두 산화 환원 반응입니다.",
    ], 0),
    ("s09", [
        "시험 포인트를 정리합니다. 첫째, 산화는 산소를 얻거나 전자를 잃는 것, 환원은 산소를 잃거나 전자를 얻는 것. 둘째, 산화와 환원은 항상 동시에 일어나고, 잃은 전자 수와 얻은 전자 수는 같다.",
        "셋째, 금속 염 수용액 반응에서는 산화된 쪽이 반응성이 큰 금속이고, 이온 수와 수용액의 색 변화를 함께 묻는다. 넷째, 광합성, 연소, 제련에서 무엇이 산화되고 무엇이 환원되는지 꼭 구분해 두세요.",
    ], 0),
    ("s10", ["오늘은 산화와 환원을 산소의 이동과 전자의 이동, 두 가지 관점으로 정리했습니다. 다음 시간에는 산과 염기, 그리고 중화 반응으로 이어집니다. 수고했어요."], 0),
]

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "narration")
os.makedirs(OUT, exist_ok=True)

async def gen():
    import edge_tts
    sem = asyncio.Semaphore(8)  # 동시 8개 — 전체 순차 대비 ~8배 빠름
    async def one(sid, k, text):
        async with sem:
            path = os.path.join(OUT, f"{sid}_{k}.mp3")
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
            print("made", f"{sid}_{k}")
    await asyncio.gather(*[one(sid, k, text)
                           for sid, segs, _ in SCENES
                           for k, text in enumerate(segs)])

asyncio.run(gen())

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(r.stdout.strip())

timing = []
files = []
t = LEAD
for sid, segs, extra in SCENES:
    scene = {"id": sid, "start": None, "segs": [], "extra": extra}
    for k, text in enumerate(segs):
        p = os.path.join(OUT, f"{sid}_{k}.mp3")
        d = dur(p)
        if scene["start"] is None:
            scene["start"] = round(t, 2)
        scene["segs"].append({"start": round(t, 2), "dur": round(d, 2), "text": text})
        files.append((p, t))
        t += d + SEG_GAP
    t += SCENE_GAP - SEG_GAP + extra
    scene["end_narration"] = round(t, 2)
    timing.append(scene)
total = round(t + 1.4, 2)

cmd = ["ffmpeg", "-y"]
for p, _ in files:
    cmd += ["-i", p]
filters, amix = [], []
for i, (p, st) in enumerate(files):
    ms = int(st * 1000)
    filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    amix.append(f"[a{i}]")
filters.append("".join(amix) + f"amix=inputs={len(files)}:normalize=0,apad=whole_dur={total}[out]")
cmd += ["-filter_complex", ";".join(filters), "-map", "[out]", "-t", str(total),
        "-b:a", "192k", os.path.join(OUT, "..", "narration.mp3")]
subprocess.run(cmd, check=True, capture_output=True)

meta = {"total": total, "scenes": timing}
with open(os.path.join(OUT, "timing.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print(json.dumps({"total": total,
                  "scenes": [{"id": s["id"], "start": s["start"],
                              "segs": [(g["start"], g["dur"]) for g in s["segs"]]}
                             for s in timing]}, ensure_ascii=False, indent=1))
