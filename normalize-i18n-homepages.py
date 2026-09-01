#!/usr/bin/env python3
"""Keep retained localized homepage sources inside the conservative evidence policy."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
I18N = ROOT / "public" / "i18n"

COPY = {
    "zh": {
        "meta": "激光切割氮氧混合设备信息，包括兼容性、供气条件、参考参数和应用评估。",
        "title": "激光切割气体混合器",
        "badge": "<span>应用评估</span> 光纤激光",
        "subtitle": "设备将氮气和氧气混合为受控辅助气体。选型前需核对机器、材料、厚度、压力、流量和供气条件。",
        "machine": ("机器", "兼容性评估"), "gas": ("供气", "压力与流量评估"), "process": ("工艺", "参考参数数据"),
        "principle": "氮氧混合设备为适用的激光切割工艺提供受控辅助气体。气体比例和结果取决于完整工况。",
        "dims": "外形尺寸、重量和多机供气能力以所供技术资料为准；多机方案还需核对同时用气、总流量、压力损失、管路、控制和接口。",
        "cut": "切割速度和断面状态取决于机器、材料、厚度、喷嘴、压力和气体比例，需要通过试切验证。",
        "compat": "兼容性应根据机器接口、压力、流量、供气和工艺要求评估，不能只按品牌或功率判断。",
        "adv": "在相同工况下比较速度、断面、用气、后处理、能耗、维护和设备兼容性。",
        "speed": ("记录数据对比", "已记录工况可作为参考，不代表其他机器或材料的通用结果。"),
        "edge": ("断面验收", "毛刺、氧化和后处理需求应按具体零件的验收标准确认。"),
        "cost": ("综合运营成本", "结合用气、周期、后处理、人工、利用率、维护和本地价格进行计算。"),
        "maint": ("维护计划", "按所供配置的说明书确认检查周期和维护项目。"),
        "multi": ("多机方案评估", "一拖三方案需核对同时用气、总流量、压力损失、管路、控制和每台机器接口。"),
        "quality": ("气体质量控制", "气源质量、调压、过滤、管路和操作都会影响污染风险。"),
        "recorded": "记录示例仅用于技术讨论，需核对完整工况和验收标准。",
        "conditional": "取决于完整工况", "baseline": "使用同机基准", "verify": "按验收标准确认", "measure": "按具体任务测量", "confirm": "确认所供技术数据",
        "estimate": "使用自有数据进行估算，并通过试切和本地运营成本验证。",
        "service": "维护和风险取决于所供配置、气体质量及使用条件，请以说明书为准。",
        "global_title": "中国供应商的出口项目支持", "global_desc": "济南钰峭机械有限公司为海外买家协调应用评估、技术沟通、报价、交付和售后支持。",
        "steps": ("应用", "集成", "交付", "支持"),
        "cta": "请提供激光功率、材料厚度、供气方案和生产目标，我们将在报价前评估适用性。",
        "faq": "结果取决于机器、材料、厚度、喷嘴、压力、流量、气体比例和断面要求。页面数据仅作参考，需验证完整工况。",
    },
    "es": {
        "meta": "Información sobre mezcladores de nitrógeno y oxígeno para corte láser: compatibilidad, suministro de gas, parámetros de referencia y evaluación de la aplicación.",
        "title": "Mezclador de gas para corte láser", "badge": "<span>Evaluación de aplicación</span> para láser de fibra",
        "subtitle": "El equipo mezcla nitrógeno y oxígeno como gas auxiliar controlado. Antes de seleccionarlo, verifique máquina, material, espesor, presión, caudal y suministro de gas.",
        "machine": ("Máquina", "Evaluación de compatibilidad"), "gas": ("Suministro", "Revisión de presión y caudal"), "process": ("Proceso", "Datos de referencia"),
        "principle": "Un mezclador de nitrógeno y oxígeno prepara un gas auxiliar controlado para procesos compatibles. La proporción y el resultado dependen de todas las condiciones del proceso.",
        "dims": "Confirme dimensiones, peso y capacidad multimáquina en los datos suministrados; revise también demanda simultánea, caudal, presión, tuberías, controles e interfaces.",
        "cut": "La velocidad y el borde dependen de la máquina, el material, el espesor, la boquilla, la presión y la proporción de gas; deben validarse con pruebas.",
        "compat": "La compatibilidad se evalúa por interfaz, presión, caudal, suministro y proceso; no puede confirmarse solo por marca o potencia.",
        "adv": "Compare velocidad, borde, consumo, acabado, energía, mantenimiento y compatibilidad bajo las mismas condiciones.",
        "speed": ("Comparaciones registradas", "Los datos registrados son referencias de caso, no resultados universales para otras máquinas o materiales."),
        "edge": ("Criterios del borde", "Confirme rebaba, oxidación y acabado según los criterios de aceptación de la pieza."),
        "cost": ("Coste total de operación", "Calcule gas, ciclo, acabado, mano de obra, utilización, mantenimiento y precios locales."),
        "maint": ("Plan de mantenimiento", "Confirme inspecciones y mantenimiento en el manual de la configuración suministrada."),
        "multi": ("Evaluación multimáquina", "Una configuración uno a tres requiere revisar demanda simultánea, caudal, presión, tuberías, controles e interfaces."),
        "quality": ("Control de calidad del gas", "La fuente, regulación, filtración, tuberías y operación influyen en el riesgo de contaminación."),
        "recorded": "Ejemplo registrado para discusión técnica; verifique todas las condiciones y criterios de aceptación.",
        "conditional": "Depende del proceso completo", "baseline": "Use la referencia de la misma máquina", "verify": "Verifique los criterios de aceptación", "measure": "Mida para el trabajo", "confirm": "Confirme los datos suministrados",
        "estimate": "Use sus propios datos para estimar y valide con pruebas de corte y costes locales.",
        "service": "El mantenimiento y el riesgo dependen de la configuración, la calidad del gas y las condiciones de uso; siga el manual.",
        "global_title": "Soporte desde China para proyectos de exportación", "global_desc": "Jinan Euchio Machinery Co., Ltd. coordina evaluación, integración, cotización, entrega y soporte para compradores internacionales.",
        "steps": ("Aplicación", "Integración", "Entrega", "Soporte"),
        "cta": "Comparta potencia, material, espesor, suministro de gas y objetivo de producción para evaluar la aplicación antes de cotizar.",
        "faq": "El resultado depende de máquina, material, espesor, boquilla, presión, caudal, proporción de gas y requisitos del borde. Los datos publicados son referencias que deben verificarse.",
    },
    "ko": {
        "meta": "레이저 절단용 질소·산소 혼합 장비의 호환성, 가스 공급 조건, 참고 파라미터 및 적용성 평가 정보입니다.",
        "title": "레이저 절단용 가스 믹서", "badge": "<span>적용성 평가</span> 파이버 레이저",
        "subtitle": "질소와 산소를 제어된 보조 가스로 혼합합니다. 선정 전 장비, 소재, 두께, 압력, 유량 및 가스 공급 조건을 확인해야 합니다.",
        "machine": ("장비", "호환성 검토"), "gas": ("가스 공급", "압력 및 유량 검토"), "process": ("공정", "참고 파라미터"),
        "principle": "질소·산소 혼합 장비는 적용 가능한 레이저 절단 공정에 제어된 보조 가스를 공급합니다. 혼합비와 결과는 전체 공정 조건에 따라 달라집니다.",
        "dims": "치수, 중량 및 다중 장비 공급 능력은 제공 기술자료에서 확인하고 동시 수요, 총 유량, 압력, 배관, 제어 및 인터페이스를 검토해야 합니다.",
        "cut": "속도와 절단면은 장비, 소재, 두께, 노즐, 압력 및 혼합비에 따라 달라지며 시험 절단으로 검증해야 합니다.",
        "compat": "호환성은 장비 인터페이스, 압력, 유량, 가스 공급 및 공정 요구사항으로 평가하며 브랜드나 출력만으로 확정할 수 없습니다.",
        "adv": "동일 조건에서 속도, 절단면, 가스 사용량, 후가공, 전력, 유지보수 및 호환성을 비교하세요.",
        "speed": ("기록 데이터 비교", "기록된 수치는 사례 참고값이며 다른 장비나 소재의 보편적 결과가 아닙니다."),
        "edge": ("절단면 기준", "버, 산화 및 후가공 요구사항은 부품의 승인 기준에 따라 확인해야 합니다."),
        "cost": ("총 운영 비용", "가스, 사이클, 후가공, 인건비, 가동률, 유지보수 및 현지 가격을 함께 계산하세요."),
        "maint": ("유지보수 계획", "공급 구성의 설명서에서 점검 주기와 유지보수 항목을 확인하세요."),
        "multi": ("다중 장비 평가", "1대 3 구성은 동시 수요, 총 유량, 압력, 배관, 제어 및 각 장비 인터페이스를 검토해야 합니다."),
        "quality": ("가스 품질 관리", "가스원, 조정, 여과, 배관 및 운전 방식이 오염 위험에 영향을 줍니다."),
        "recorded": "기술 검토용 기록 사례이며 전체 공정 조건과 승인 기준을 확인해야 합니다.",
        "conditional": "전체 공정에 따라 다름", "baseline": "동일 장비 기준 사용", "verify": "승인 기준으로 확인", "measure": "작업별 측정", "confirm": "공급 기술자료 확인",
        "estimate": "자체 데이터로 추정하고 시험 절단과 현지 운영 비용으로 검증하세요.",
        "service": "유지보수와 위험은 구성, 가스 품질 및 사용 조건에 따라 달라지므로 설명서를 따르세요.",
        "global_title": "중국 기반 수출 프로젝트 지원", "global_desc": "Jinan Euchio Machinery Co., Ltd.는 해외 구매자의 적용성 검토, 통합, 견적, 납품 및 지원을 조율합니다.",
        "steps": ("적용", "통합", "납품", "지원"),
        "cta": "레이저 출력, 소재, 두께, 가스 공급 및 생산 목표를 보내주시면 견적 전에 적용성을 검토합니다.",
        "faq": "결과는 장비, 소재, 두께, 노즐, 압력, 유량, 혼합비 및 절단면 요구사항에 따라 달라집니다. 공개 데이터는 검증이 필요한 참고값입니다.",
    },
    "ja": {
        "meta": "レーザー切断用の窒素・酸素混合装置について、互換性、ガス供給条件、参考パラメータ、用途評価の情報を提供します。",
        "title": "レーザー切断用ガスミキサー", "badge": "<span>用途評価</span> ファイバーレーザー",
        "subtitle": "窒素と酸素を制御されたアシストガスとして混合します。選定前に、機械、材料、板厚、圧力、流量、ガス供給条件を確認してください。",
        "machine": ("機械", "互換性確認"), "gas": ("ガス供給", "圧力・流量確認"), "process": ("工程", "参考パラメータ"),
        "principle": "窒素・酸素混合装置は、適合するレーザー切断工程に制御されたアシストガスを供給します。混合比と結果は工程条件全体に依存します。",
        "dims": "寸法、重量、複数機への供給能力は提供仕様で確認し、同時需要、総流量、圧力、配管、制御、各機械の接続も検討してください。",
        "cut": "速度と切断面は、機械、材料、板厚、ノズル、圧力、混合比に依存し、試し切りでの検証が必要です。",
        "compat": "互換性は機械インターフェース、圧力、流量、ガス供給、工程要件から評価し、ブランドや出力だけでは確定できません。",
        "adv": "同じ条件で速度、切断面、ガス使用量、後処理、電力、保守、互換性を比較してください。",
        "speed": ("記録データの比較", "記録値は事例の参考であり、他の機械や材料に共通する結果ではありません。"),
        "edge": ("切断面の基準", "バリ、酸化、後処理の要否を部品の受入基準に従って確認してください。"),
        "cost": ("総運用コスト", "ガス、サイクル、後処理、労務、稼働率、保守、現地価格を合わせて計算します。"),
        "maint": ("保守計画", "供給構成の取扱説明書で点検周期と保守項目を確認してください。"),
        "multi": ("複数機の評価", "1対3構成は同時需要、総流量、圧力、配管、制御、各機械の接続を確認する必要があります。"),
        "quality": ("ガス品質管理", "ガス源、調圧、ろ過、配管、運用が汚染リスクに影響します。"),
        "recorded": "技術検討用の記録例です。工程条件全体と受入基準を確認してください。",
        "conditional": "工程条件全体に依存", "baseline": "同一機械の基準を使用", "verify": "受入基準で確認", "measure": "作業ごとに測定", "confirm": "供給仕様を確認",
        "estimate": "自社データで試算し、試し切りと現地の運用コストで検証してください。",
        "service": "保守とリスクは構成、ガス品質、使用条件に依存します。取扱説明書に従ってください。",
        "global_title": "中国拠点の輸出プロジェクト支援", "global_desc": "Jinan Euchio Machinery Co., Ltd. は海外購入者向けに用途評価、統合、見積、納入、サポートを調整します。",
        "steps": ("用途", "統合", "納入", "支援"),
        "cta": "レーザー出力、材料、板厚、ガス供給、製造目標を共有してください。見積前に用途を評価します。",
        "faq": "結果は機械、材料、板厚、ノズル、圧力、流量、混合比、切断面要件に依存します。公開データは検証が必要な参考値です。",
    },
    "pt": {
        "meta": "Informações sobre mistura de nitrogênio e oxigênio para corte a laser: compatibilidade, fornecimento de gás, parâmetros de referência e avaliação da aplicação.",
        "title": "Misturador de gás para corte a laser", "badge": "<span>Avaliação da aplicação</span> para laser de fibra",
        "subtitle": "O equipamento mistura nitrogênio e oxigênio como gás auxiliar controlado. Antes da seleção, verifique máquina, material, espessura, pressão, vazão e fornecimento de gás.",
        "machine": ("Máquina", "Avaliação de compatibilidade"), "gas": ("Fornecimento", "Revisão de pressão e vazão"), "process": ("Processo", "Dados de referência"),
        "principle": "Um misturador de nitrogênio e oxigênio prepara gás auxiliar controlado para processos compatíveis. A proporção e o resultado dependem de todas as condições do processo.",
        "dims": "Confirme dimensões, peso e capacidade multimáquina nos dados fornecidos; revise também demanda simultânea, vazão, pressão, tubulação, controles e interfaces.",
        "cut": "A velocidade e a borda dependem da máquina, material, espessura, bico, pressão e proporção do gás; valide com testes.",
        "compat": "A compatibilidade é avaliada pela interface, pressão, vazão, fornecimento e processo; não pode ser confirmada apenas por marca ou potência.",
        "adv": "Compare velocidade, borda, consumo, acabamento, energia, manutenção e compatibilidade nas mesmas condições.",
        "speed": ("Comparações registradas", "Dados registrados são referências de caso, não resultados universais para outras máquinas ou materiais."),
        "edge": ("Critérios da borda", "Confirme rebarba, oxidação e acabamento conforme os critérios de aceitação da peça."),
        "cost": ("Custo total de operação", "Calcule gás, ciclo, acabamento, mão de obra, utilização, manutenção e preços locais."),
        "maint": ("Plano de manutenção", "Confirme inspeções e manutenção no manual da configuração fornecida."),
        "multi": ("Avaliação multimáquina", "Uma configuração um para três exige revisar demanda simultânea, vazão, pressão, tubulação, controles e interfaces."),
        "quality": ("Controle da qualidade do gás", "Fonte, regulagem, filtragem, tubulação e operação influenciam o risco de contaminação."),
        "recorded": "Exemplo registrado para discussão técnica; verifique todas as condições e critérios de aceitação.",
        "conditional": "Depende do processo completo", "baseline": "Use a referência da mesma máquina", "verify": "Verifique os critérios de aceitação", "measure": "Meça para o trabalho", "confirm": "Confirme os dados fornecidos",
        "estimate": "Use seus próprios dados para estimar e valide com testes de corte e custos locais.",
        "service": "A manutenção e o risco dependem da configuração, qualidade do gás e condições de uso; siga o manual.",
        "global_title": "Suporte da China para projetos de exportação", "global_desc": "Jinan Euchio Machinery Co., Ltd. coordena avaliação, integração, cotação, entrega e suporte para compradores internacionais.",
        "steps": ("Aplicação", "Integração", "Entrega", "Suporte"),
        "cta": "Informe potência, material, espessura, fornecimento de gás e objetivo de produção para avaliar a aplicação antes da cotação.",
        "faq": "O resultado depende de máquina, material, espessura, bico, pressão, vazão, proporção do gás e requisitos da borda. Os dados publicados são referências que precisam ser verificadas.",
    },
}


def normalize(lang, data):
    c = COPY[lang]
    data["meta"]["ogDescription"] = c["meta"]
    data["hero"].update({
        "badge": c["badge"], "title": c["title"], "subtitle": c["subtitle"],
        "statSpeedValue": c["machine"][0], "statSpeedLabel": c["machine"][1],
        "statBurrsValue": c["gas"][0], "statBurrsLabel": c["gas"][1],
        "statGasValue": c["process"][0], "statGasLabel": c["process"][1],
    })
    data["principle"].update({
        "description": c["principle"], "dimsDesc": c["dims"],
        "cutEffectDesc": c["cut"], "compatDesc": c["compat"],
    })
    data["advantages"].update({
        "description": c["adv"],
        "speedTitle": c["speed"][0], "speedDesc": c["speed"][1],
        "burrsTitle": c["edge"][0], "burrsDesc": c["edge"][1],
        "costTitle": c["cost"][0], "costDesc": c["cost"][1],
        "maintTitle": c["maint"][0], "maintDesc": c["maint"][1],
        "oneToTwoTitle": c["multi"][0], "oneToTwoDesc": c["multi"][1],
        "lensTitle": c["quality"][0], "lensDesc": c["quality"][1],
    })
    comparison = data["comparison"]
    comparison["speedRow"][1:] = [c["recorded"], c["baseline"], c["conditional"], c["conditional"]]
    comparison["surfaceRow"][1:] = [c["verify"], c["verify"], c["conditional"], c["conditional"]]
    comparison["gasRow"][1:] = [c["measure"], c["measure"], c["measure"], c["measure"]]
    comparison["powerRow"][1:] = [c["confirm"], c["conditional"], c["conditional"], c["confirm"]]
    comparison["holeRow"][1:] = [c["verify"], c["verify"], c["verify"], c["verify"]]
    comparison["protectionRow"][1:] = [c["confirm"], c["confirm"], c["confirm"], c["confirm"]]
    data["roi"]["description"] = c["estimate"]
    data["airPain"].update({
        "pain1Item4": c["service"], "pain1Solution": c["confirm"], "pain1Cost": c["estimate"],
        "pain2Solution": c["verify"], "pain2Cost": c["conditional"],
        "pain3Item3": c["service"], "pain3Solution": c["confirm"], "pain3Cost": c["conditional"],
        "summaryTitle": c["cost"][0], "summaryText": c["cost"][1],
    })
    data["params"]["description"] = c["recorded"]
    data["params"]["best12kw"] = c["recorded"]
    data["params"]["best20kw"] = c["recorded"]
    data["params"]["best30kw"] = c["recorded"]
    data["samples"]["label"] = c["recorded"]
    data["samples"]["description"] = c["recorded"]
    for key in ("desc12kw30kw", "desc30kw", "desc60kw", "desc12kwAlu3", "desc12kwAlu2", "desc12kwAlu1"):
        data["samples"][key] = c["recorded"]
    steps = c["steps"]
    data["globalPresence"].update({
        "label": c["global_title"], "title": c["global_title"], "description": c["global_desc"],
        "asia": steps[0], "europe": steps[1], "americas": steps[2], "oceania": steps[3],
        "statCountries": steps[0], "statContinents": steps[1], "statPower": steps[2], "statProduction": steps[3],
        "badgeAsia": steps[0], "badgeEurope": steps[1], "badgeAmericas": steps[2], "badgeOceania": steps[3],
        "ctaTitle": c["global_title"], "ctaDesc": c["cta"],
    })
    data["cta"]["title"] = c["global_title"]
    data["cta"]["description"] = c["cta"]
    for key in ("a1", "a3", "a4", "a7"):
        data["faq"][key] = c["faq"]
    data["faq"]["a5"] = c["service"]
    data["faq"]["a8"] = c["service"]
    return data


def main():
    for lang in COPY:
        path = I18N / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        normalized = normalize(lang, data)
        path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
