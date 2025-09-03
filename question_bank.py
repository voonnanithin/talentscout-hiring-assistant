from typing import List, Dict

QUESTION_BANK = {
    "python": [
        "Explain the difference between a list, tuple, and set. When would you use each?",
        "How do generators differ from list comprehensions and when are they preferable?",
        "What are common pitfalls with mutable default arguments in functions?",
        "How does the GIL impact multithreading in Python and how can you work around it?",
        "Describe how you'd structure a project for packaging and dependency management."
    ],
    "django": [
        "How do Django ORM querysets evaluate lazily and why does that matter?",
        "What’s the difference between function-based and class-based views, and when would you choose one over the other?",
        "How do you handle N+1 query issues in Django and optimize database access?",
        "Explain Django’s middleware and a scenario where you’d write custom middleware.",
        "How do you manage settings and secrets across environments in Django projects?"
    ],
    "sql": [
        "Explain normalization vs denormalization and when each is appropriate.",
        "How would you detect and resolve a slow query? Mention indexes and query plans.",
        "Difference between INNER JOIN, LEFT JOIN, and CROSS JOIN with examples.",
        "What is a transaction isolation level and why does it matter?",
        "How do window functions work and when would you use them?"
    ],
    "javascript": [
        "Explain event loop and microtask queue in JavaScript.",
        "Compare var, let, and const, and scoping implications.",
        "How does prototypal inheritance work?",
        "What are closures and common use-cases?",
        "Explain debouncing vs throttling and when to use each."
    ],
    "react": [
        "What problems do hooks solve compared to class components?",
        "Explain reconciliation and keys in lists.",
        "How do you manage state at scale? Compare Context, Redux, and server cache libraries.",
        "What are Suspense and concurrent features used for?",
        "How do you optimize renders and bundle size?"
    ],
    "docker": [
        "Explain the difference between images and containers.",
        "How do you write a multi-stage Dockerfile and why?",
        "What strategies do you use to keep image size small?",
        "How do you handle secrets and environment variables in containers?",
        "Describe common networking modes and when to use them."
    ],
    "kubernetes": [
        "What are Deployments vs StatefulSets and when would you use each?",
        "Explain Services, Ingress, and how traffic reaches a pod.",
        "How do you configure liveness/readiness probes?",
        "What is a ConfigMap vs Secret and typical patterns to use them?",
        "How do you roll out zero-downtime updates?"
    ],
    "machine learning": [
        "How do you handle class imbalance beyond resampling (e.g., metrics, thresholds)?",
        "What’s the bias-variance tradeoff and how do you diagnose it?",
        "Compare L1 vs L2 regularization and their effects.",
        "How do you validate time-series models properly?",
        "What steps ensure reproducibility in ML experiments?"
    ]
}

def fallback_questions(tech_stack: List[str], per_tech: int = 2, max_total: int = 5) -> List[str]:
    techs = [t.lower() for t in tech_stack]
    picked: List[str] = []
    for t in techs:
        bank = None
        # fuzzy contains match
        for key in QUESTION_BANK.keys():
            if key in t:
                bank = QUESTION_BANK[key]
                break
        if bank:
            picked.extend(bank[:per_tech])
        if len(picked) >= max_total:
            break
    if not picked:
        picked = [
            "Describe a challenging technical problem you solved recently and your approach.",
            "How do you ensure code quality and maintainability in team projects?",
            "Explain a time you optimized performance—what was the baseline, the change, and the impact?",
            "How do you design tests for complex features or systems?",
            "Walk through a project architecture you would propose for the desired role."
        ]
    return picked[:max_total]
