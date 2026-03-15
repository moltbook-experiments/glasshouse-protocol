# Agent skillset categories for UAT simulation

SKILLSET_CATEGORIES = {
    # Technical Skills
    'data_analysis': {
        'description': 'Statistical analysis, data cleaning, visualization',
        'category': 'technical'
    },
    'content_generation': {
        'description': 'Text writing, creative content, documentation',
        'category': 'technical'
    },
    'image_processing': {
        'description': 'Image recognition, manipulation, computer vision',
        'category': 'technical'
    },
    'code_development': {
        'description': 'Programming, debugging, code review',
        'category': 'technical'
    },
    'research_synthesis': {
        'description': 'Information gathering, literature review',
        'category': 'technical'
    },
    'automation': {
        'description': 'Workflow optimization, script creation',
        'category': 'technical'
    },
    'translation': {
        'description': 'Language translation, localization',
        'category': 'technical'
    },
    'security_analysis': {
        'description': 'Vulnerability scanning, threat detection',
        'category': 'technical'
    },
    'financial_modeling': {
        'description': 'Economic analysis, forecasting',
        'category': 'technical'
    },
    'customer_service': {
        'description': 'Query handling, support automation',
        'category': 'technical'
    },

    # A2A Service Skills
    'trust_reputation': {
        'description': 'Verifiable identity, credit scoring, proof-of-computation',
        'category': 'a2a_service'
    },
    'micropayments': {
        'description': 'Nanopayment processing, escrow services',
        'category': 'a2a_service'
    },
    'specialized_labor': {
        'description': 'Security red teaming, data janitorial services',
        'category': 'a2a_service'
    },
    'human_loop': {
        'description': 'CAPTCHA solving, compliance notarization',
        'category': 'a2a_service'
    },
    'governance': {
        'description': 'Real-time observability, legal mapping',
        'category': 'a2a_service'
    }
}

PROFICIENCY_LEVELS = ['beginner', 'intermediate', 'expert']

JOB_TYPES = {
    'data_processing': {
        'required_skills': ['data_analysis'],
        'complexity': 2.0,
        'base_payment': 10,
        'data_locality': 'local',  # local, regional, global
        'hardware_requirements': ['cpu']
    },
    'content_creation': {
        'required_skills': ['content_generation'],
        'complexity': 1.5,
        'base_payment': 8,
        'data_locality': 'global',
        'hardware_requirements': ['cpu']
    },
    'code_review': {
        'required_skills': ['code_development'],
        'complexity': 2.5,
        'base_payment': 12,
        'data_locality': 'global',
        'hardware_requirements': ['cpu']
    },
    'security_audit': {
        'required_skills': ['security_analysis'],
        'complexity': 3.0,
        'base_payment': 15,
        'data_locality': 'local',
        'hardware_requirements': ['cpu', 'network_access']
    },
    'identity_verification': {
        'required_skills': ['trust_reputation'],
        'complexity': 1.0,
        'base_payment': 5,
        'data_locality': 'regional',
        'hardware_requirements': ['cpu', 'api_access']
    },
    'payment_processing': {
        'required_skills': ['micropayments'],
        'complexity': 0.5,
        'base_payment': 2,
        'data_locality': 'global',
        'hardware_requirements': ['cpu']
    },
    'compliance_check': {
        'required_skills': ['governance'],
        'complexity': 2.0,
        'base_payment': 10,
        'data_locality': 'regional',
        'hardware_requirements': ['cpu', 'legal_database_access']
    },
    'gpu_rendering': {
        'required_skills': ['image_processing'],
        'complexity': 4.0,
        'base_payment': 20,
        'data_locality': 'local',
        'hardware_requirements': ['gpu']
    },
    'iot_actuation': {
        'required_skills': ['automation'],
        'complexity': 1.0,
        'base_payment': 8,
        'data_locality': 'local',
        'hardware_requirements': ['iot_controller']
    }
}

def get_skillsets_by_category(category: str) -> list:
    """Get all skillsets in a specific category."""
    return [skill for skill, info in SKILLSET_CATEGORIES.items() if info['category'] == category]

def get_random_skillsets(count: int = 3) -> list:
    """Get random skillsets for agent assignment."""
    import random
    all_skills = list(SKILLSET_CATEGORIES.keys())
    return random.sample(all_skills, min(count, len(all_skills)))