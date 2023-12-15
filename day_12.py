import re

MEMO = {}


class IntactRecord:
    def __init__(self, intact_line):
        self.intact_line = intact_line

    def to_replica_group(self, max_idx=None):
        return [len(group) for group in re.findall(r'([#?]+)', self.intact_line[:max_idx])]

    def unfold(self):
        self.intact_line = self.intact_line + (4 * f"?{self.intact_line}")

    def copy(self):
        return IntactRecord(str(self.intact_line))

    def __str__(self):
        return self.intact_line


class MaintenanceReport:
    def __init__(self, intact_record: IntactRecord, replica_group: list):
        self.intact_record = intact_record
        self.replica_group = replica_group

    def __str__(self):
        return f"Report {self.intact_record} {self.replica_group}"

    def unfold(self):
        self.intact_record.unfold()
        self.replica_group = self.replica_group * 5

    def calculate_combinations(self):
        return self._calc_combinations(self.intact_record.intact_line, self.replica_group)

    def _calc_combinations_cached(self, report, replica_group):
        if str((report, replica_group)) in MEMO:
            return MEMO[str((report, replica_group))]
        return self._calc_combinations(report, replica_group)

    def _calc_combinations(self, report, replica_group):
        if '?' not in report:
            calculated_replicas = [len(group) for group in report.split('.') if len(group) > 0]
            result = 1 if calculated_replicas == replica_group else 0
            MEMO[str((report, replica_group))] = result
            return result

        qm_idx = report.index('?')

        pre_replica_groups = [group for group in report[:qm_idx].split('.')]

        idx = 0
        for group in pre_replica_groups[:-1]:
            if len(group) != 0:
                if idx >= len(replica_group) or len(group) != replica_group[idx]:
                    return 0
                idx += 1

        pre_str = pre_replica_groups[-1] if len(pre_replica_groups) > 0 else ''

        new_report = pre_str + '#' + report[qm_idx + 1:]
        new_replica = replica_group[idx:]

        hash_combinations = self._calc_combinations_cached(new_report, new_replica)
        dot_combinations = self._calc_combinations_cached(pre_str + '.' + report[qm_idx + 1:], replica_group[idx:])

        MEMO[str((report, replica_group))] = hash_combinations + dot_combinations
        return hash_combinations + dot_combinations


with open('input/day_12.txt') as file:
    reports = []
    for line in file.readlines():
        intact_report_line, replica_line = line.split(' ')
        intact_report = IntactRecord(intact_report_line)
        replica_set = [int(val.strip()) for val in replica_line.split(',')]

        new_report = MaintenanceReport(intact_report, replica_set)
        new_report.unfold()
        reports.append(new_report)

    print(sum([report.calculate_combinations() for report in reports]))
