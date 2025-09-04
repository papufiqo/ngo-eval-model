import pandas as pd
import numpy as np
import yaml

class NGOScorecard:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.scores = {}

    def goal_achievement_index(self, data):
        w = self.config['weights']['goal_achievement']
        activity_completion = (data['completed_activities'] / data['planned_activities']) * 100
        alignment = 100 if data['cerv_alignment'] else 0
        policy = data['policy_outcomes_score'] * 20  # 0–100 scale
        recs = (data['recommendations_2023_addressed'] / data['total_recommendations']) * 100 if data['total_recommendations'] > 0 else 0

        gai = (
            activity_completion * w['activity_completion'] +
            alignment * w['alignment_with_cerv'] +
            policy * w['policy_outcomes'] +
            recs * w['implementation_of_2023_rec']
        )
        self.scores['GAI'] = round(gai, 2)
        return self.scores['GAI']

    def work_capacity_index(self, data):
        w = self.config['weights']['work_capacity']
        efficiency = data['budget_efficiency_ratio'] * 100
        monitoring = self.config['scoring']['rubric_5point'][data['monitoring_framework_score']] * 20
        risk_ethics = 100 if data['risk_management_present'] and not data['ethics_issues_identified'] else 0
        capacity = ((data['training_sessions'] / 10) * 50 + data['avg_satisfaction'] * 10) / 2  # normalized
        youth = data['youth_network_support_score'] * 20

        wci = (
            efficiency * w['resource_efficiency'] / 100 +
            monitoring * w['monitoring_quality'] / 100 +
            risk_ethics * w['risk_ethics'] / 100 +
            capacity * w['capacity_building'] / 100 +
            youth * w['youth_support'] / 100
        ) * 100
        self.scores['WCI'] = round(wci, 2)
        return self.scores['WCI']

    def added_value_index(self, data):
        w = self.config['weights']['added_value']
        policy = min(data['policy_citations'] + data['eu_meetings_attended'], 100)
        engagement = min((data['partner_organisations'] / 20) * 100, 100)
        reach = (data['social_media_impressions'] / 500000) * 100
        accessibility = (data['accessible_content_percentage'] / 100) * 100
        communication = (reach * 0.6 + accessibility * 0.4)
        innovation = data['project_innovation_score'] * 20

        avi = (
            policy * w['policy_influence'] / 100 +
            engagement * w['stakeholder_engagement'] / 100 +
            communication * w['communication_reach'] / 100 +
            innovation * w['project_innovation'] / 100
        ) * 100
        self.scores['AVI'] = round(avi, 2)
        return self.scores['AVI']

    def inclusiveness_audit(self, data):
        criteria = [
            data['disabled_leadership'],
            data['youth_involvement'],
            data['all_materials_accessible'],
            data['intersectional_approach'],
            data['ethical_research']
        ]
        compliant = all(criteria)
        missing = []
        labels = ["Disabled Leadership", "Youth Involvement", "Accessibility", "Intersectionality", "Ethical Research"]
        for i, met in enumerate(criteria):
            if not met:
                missing.append(labels[i])
        return {"compliant": compliant, "missing": missing}

    def get_scores(self):
        return self.scores
