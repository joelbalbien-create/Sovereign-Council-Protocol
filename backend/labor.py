import asyncio, os

LABOR_CONFIGS = {
    'workforce': {
        'alethea': {'role': 'Skills and Market Analyst', 'task': 'Analyze skills, experience, education. Map to labor market data. Identify transferable skills. Quantify retraining ROI.'},
        'sophia':  {'role': 'Industry and Macro Strategist', 'task': 'Analyze macro trends in current industry. Identify growth sectors. Which industries are hiring vs contracting?'},
        'eirene':  {'role': 'Risk and Geography Analyst', 'task': 'Identify career change risks. Top 3-5 geographic opportunities by opportunity vs cost of living. What are transition risks?'},
        'kairos':  {'role': 'Human Dimension and Wisdom', 'task': 'What path honors this persons dignity and fulfillment? What do numbers miss? Wise path balancing financial reality with human flourishing.'},
    },
    'medical': {
        'alethea': {'role': 'Clinical Data Analyst', 'task': 'Analyze clinical data and lab values. Quantitative risk factors and probabilities.'},
        'sophia':  {'role': 'Treatment Landscape Strategist', 'task': 'Survey treatment landscape and research. What options exist? What does literature indicate?'},
        'eirene':  {'role': 'Risk and Contraindication Analyst', 'task': 'Identify risks, contraindications, drug interactions. What warning signs need attention?'},
        'kairos':  {'role': 'Patient Values and Quality of Life', 'task': 'What matters most beyond clinical outcomes? How do values affect the decision?'},
    },
    'legal': {
        'alethea': {'role': 'Case Law and Precedent Analyst', 'task': 'Analyze case law, statutes, precedents. What do historical outcomes show?'},
        'sophia':  {'role': 'Jurisdictional Strategist', 'task': 'Survey jurisdictional landscape. How do courts approach this? What strategic options exist?'},
        'eirene':  {'role': 'Risk and Exposure Analyst', 'task': 'Identify legal risks, exposure, downside scenarios. What contingencies are needed?'},
        'kairos':  {'role': 'Equity and Human Dimension', 'task': 'What is the just outcome beyond what is strictly legal? What human factors should inform strategy?'},
    },
    'financial': {
        'alethea': {'role': 'Quantitative Financial Analyst', 'task': 'Analyze financial data. Portfolio, assets, liabilities, projections. What does rigorous analysis recommend?'},
        'sophia':  {'role': 'Macro Economic Strategist', 'task': 'Provide macro economic context. How do current conditions affect this situation?'},
        'eirene':  {'role': 'Downside and Sequence Risk Analyst', 'task': 'Identify sequence risk, downside scenarios, concentration risks. What hedges are indicated?'},
        'kairos':  {'role': 'Values Legacy and Life Stage Wisdom', 'task': 'What are deeper financial values and legacy goals? How does life stage affect strategy?'},
    },
    'general': {
        'alethea': {'role': 'Quantitative Analyst', 'task': 'Analyze quantitative and data-driven dimensions. Be specific and evidence-based.'},
        'sophia':  {'role': 'Strategic Context Analyst', 'task': 'Analyze broader strategic and macro dimensions. What forces shape this situation?'},
        'eirene':  {'role': 'Risk Analyst', 'task': 'Identify key risks, failure modes, downside scenarios. What could go wrong?'},
        'kairos':  {'role': 'Wisdom and Human Dimension', 'task': 'What is the wise human-centered perspective? What do data and strategy miss?'},
    }
}

def detect_labor_domain(query, domain, resume_text=None):
    q = query.lower()
    if resume_text or any(w in q for w in ['resume','job','career','unemployed','laid off','replaced','workforce','retraining','occupation','automation']):
        return 'workforce'
    if any(w in q for w in ['diagnosis','treatment','medication','symptoms','patient','clinical','medical']):
        return 'medical'
    if any(w in q for w in ['lawsuit','legal','contract','liability','court','attorney','settlement']):
        return 'legal'
    if any(w in q for w in ['portfolio','investment','retirement','savings','financial plan','wealth']):
        return 'financial'
    return domain if domain in LABOR_CONFIGS else 'general'

async def run_labor_division(query, domain, resume_text, call_openai, call_anthropic, call_gemini, call_grok):
    labor_domain = detect_labor_domain(query, domain, resume_text)
    config = LABOR_CONFIGS[labor_domain]
    context = 'Query: ' + query
    if resume_text:
        context += '\n\nResume:\n' + resume_text

    def build_prompt(name):
        r = config[name]['role']
        t = config[name]['task']
        return 'You are ' + name.capitalize() + ', ' + r + ' on the Sovereign Council.\n\nAssignment: ' + t + '\n\n' + context + '\n\n2-3 paragraphs. Your assigned domain only.'

    async def safe_call(fn, prompt, system, timeout=120):
        try:
            return await asyncio.wait_for(fn(prompt, system), timeout=timeout)
        except Exception:
            return None

    systems = {k: 'You are ' + k.capitalize() + ', ' + config[k]['role'] + ' on the Sovereign Council.' for k in config}
    r = await asyncio.gather(
        safe_call(call_openai,    build_prompt('alethea'), systems['alethea']),
        safe_call(call_gemini,    build_prompt('sophia'),  systems['sophia']),
        safe_call(call_grok,      build_prompt('eirene'),  systems['eirene']),
        safe_call(call_anthropic, build_prompt('kairos'),  systems['kairos']),
    )
    analyses = {
        'alethea': r[0] or 'unavailable',
        'sophia':  r[1] or 'unavailable',
        'eirene':  r[2] or 'unavailable',
        'kairos':  r[3] or 'unavailable',
    }
    active = sum(1 for v in analyses.values() if 'unavailable' not in v.lower())
    if active < 2:
        return {'error': 'Insufficient queens', 'queens_active': active, 'status': 'FAILED'}

    parts = []
    parts.append('Sovereign Council Fusion Engine - Division of Labor.')
    parts.append('Query: ' + query)
    parts.append('Domain: ' + labor_domain)
    parts.append('')
    for k in analyses:
        parts.append(k.upper() + ' (' + config[k]['role'] + '):')
        parts.append(analyses[k][:600])
        parts.append('')
    parts.append('Synthesize into:')
    parts.append('## 1. SOVEREIGN RECOMMENDATION')
    parts.append('## 2. PRIORITY ACTION PLAN (3 steps with timeframes)')
    parts.append('## 3. HONEST TENSIONS')
    fusion_prompt = chr(10).join(parts)

    try:
        import anthropic as sdk
        client = sdk.AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        resp = await asyncio.wait_for(
            client.messages.create(
                model='claude-sonnet-4-5', max_tokens=2500,
                system='Sovereign Council Fusion Engine. Integrate four expert analyses into one unified recommendation. Be specific and actionable.',
                messages=[{'role': 'user', 'content': fusion_prompt}]
            ), timeout=120)
        fusion_text = resp.content[0].text
    except Exception as e:
        fusion_text = 'Fusion unavailable: ' + str(e)

    return {
        'mode': 'division_of_labor',
        'labor_domain': labor_domain,
        'queen_analyses': analyses,
        'queens_active': active,
        'fusion': {
            'fusion_answer': fusion_text,
            'status': 'SOVEREIGN_RECOMMENDATION',
            'confidence': round(active / 4, 2),
            'queens_active': active
        },
        'labor_assignments': {k: v['role'] for k, v in config.items()}
    }
