import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.power import TTestPower, TTestIndPower

class Utilities:
    @staticmethod
    def t_to_d(t, n):
        return t / (n ** 0.5)

    @staticmethod
    def calc_required_sample_size(d, power, alpha=0.05, tail='two-sided'):
        analysis = TTestPower()
        return analysis.solve_power(effect_size=d, alpha=alpha, nobs=None, power=power, alternative=tail)

    @staticmethod
    def calc_post_hoc_power(n, d, alpha=0.05, tail='two-sided'):
        analysis = TTestPower()
        return analysis.solve_power(effect_size=d, alpha=alpha, nobs=n, power=None, alternative=tail)

    @staticmethod
    def dereferencify(x):
        if 'C(' in x:
            return f'{x.split("C(")[1].split(",")[0]}[{x.split("[")[1].split("]")[0]}]'
        else:
            return x

    @staticmethod
    def represents_int(s):
        try:
            int(s)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def first_matching(iterable, condition=lambda x: True):
        return next(x for x in iterable if condition(x))

class StatsHandler:
    def __init__(self, data=None):
        self._test_objective = "independent"
        self._tail = "two-sided"
        self.reg_results = None
        self._alpha = 0.05
        self._permutation_count = 10000
        self._test_type = "rank"
        self._data = None
        self._query_column = None
        self._query_on_column = False
        self._identifier2 = None
        self._identifier1 = None
        self._measuring_column = None
        self._english_measuring = None
        self._is_regression_spec = False
        self._regression_lhs = None
        self._regression_rhs = []
        self._regression_rhs_names = []
        self._override_cohens_d = None
        self._override_n = None
        self._override_t = None
        self._override_n2 = None
        self._override_power = None
        self._sigfig = 3

        if data is not None:
            self.set_data(data)

    def set_data(self, data):
        self._data = data
        return self

    def set_p(self, value):
        self._alpha = value
        return self

    def is_paired(self):
        self._test_objective = "paired"
        self._data['Difference'] = self.data2 - self.data1
        return self

    def using_rank(self):
        self._test_type = "rank"
        return self

    def measuring(self, english_name):
        self._english_measuring = english_name
        return self

    def using_permutation(self, permutation_count=10000):
        self._test_type = "permutation"
        self._permutation_count = permutation_count
        return self

    def _get_data(self, identifier):
        if self._query_on_column:
            data_here = self._data.query(self._query_column + ' == "' + identifier + '"')

            if self._measuring_column is not None:
                return data_here[self._measuring_column]
            else:
                return data_here
        else:
            return self._data[identifier]

    @property
    def sse(self):
        if not self.reg_results:
            return None

        return sum([i ** 2 for i in self.reg_results.resid])

    @property
    def intercept(self):
        x_bar = self.data1.mean()
        y_bar = self.data2.mean()

        return y_bar - self.slope * x_bar

    @property
    def slope(self):
        s_x = self.data1.std()
        s_xy = self.data1.cov(self.data2)

        return s_xy / (s_x ** 2)

    @property
    def equation(self):
        return f'{self.round(self.intercept)} = ȳ - {self.round(self.slope)}x̄'

    @property
    def safe_value_map(self):
        return np.array([not np.isnan(self.data1[i]) and not np.isnan(self.data2[i]) for i in range(len(self.data1))])

    def regress_to(self, column):
        self._is_regression_spec = True
        self._regression_lhs = column
        self._regression_rhs = []
        self._regression_rhs_names = []

        return self

    def add_regression_component(self, column, reference=None):
        self._regression_rhs_names.append(column)

        if reference is not None:
            self._regression_rhs.append(f'C({column}, Treatment(reference="{reference}"))')
        else:
            self._regression_rhs.append(column)

        return self

    def add_interaction_term(self, column1, column2, add_main_effects = True):
        self._regression_rhs.append(f'{column1}{"*" if add_main_effects else ":"}{column2}')
        self._regression_rhs_names.append(None)
        return self

    def apply_regression_formula(self, formula):
        reg_formula = sm.regression.linear_model.OLS.from_formula(data=self._data, formula=formula)
        reg_results = reg_formula.fit()
        self._data['resid'] = reg_results.resid
        self._data['fitted'] = reg_results.fittedvalues
        self.reg_results = reg_results

        return reg_results.summary()

    @property
    def regression_formula_stub(self):
        return f'{self._regression_lhs} ~ B0 + {" ".join([f"B{i + 1}*{e}" for i, e in enumerate(self._regression_rhs_names)])}'

    def predict_using_regression(self, values, allow_missing_values = False):
        data_source = self.reg_results.summary().tables[1].data[1:]
        columns = [[Utilities.dereferencify(x[0].strip()), float(x[1].strip())] for x in data_source if x[0].strip() != '' and '*' not in x[0] and ':' not in x[0] and 'Intercept' not in x[0]]
        column_lookup = { k[0]: k[1] for k in columns }

        intercept = float(data_source[0][1].strip())

        for entry in values:
            if entry not in self._regression_rhs_names:
                raise ValueError(f'Invalid/unknown column specified: {entry}')

        if not allow_missing_values:
            for entry in self._regression_rhs_names:
                if entry not in values:
                    raise ValueError(f'Missing column: {entry}')

        print('Using equation of form:')
        print(self.regression_formula_stub)

        equation_components = []
        for entry in values:
            if Utilities.represents_int(values[entry]):
                equation_components.append([column_lookup[entry], values[entry], f'coef({entry})'])
            else:
                entry_name = f"{entry}[T.{values[entry]}]"
                if entry_name in column_lookup:
                    equation_components.append([column_lookup[entry_name], 1, f'coef({entry_name})'])
                else:
                    pulling_instead_on = None
                    for key in column_lookup:
                        if key.startswith(f'{entry}[T.'):
                            pulling_instead_on = key
                            break

                    if pulling_instead_on is None:
                        raise ValueError(f'Unresolved value for {entry}: {values[entry]}')

                    equation_components.append([column_lookup[pulling_instead_on], 0, f'coef({pulling_instead_on})'])

        print('Using:')
        print(f"{self._regression_lhs} = intercept + {' + '.join([f'{x[2]}*{x[1]}' for x in equation_components])}")
        print(f"   = {intercept} + {' + '.join([f'{x[0]}*{x[1]}' for x in equation_components])}")

        res = intercept
        for x in equation_components:
            res += x[0] * x[1]
        print(f'\n= {self.round(res)}')

        return res

    def do_regression(self):
        na_map = self.safe_value_map

        x = np.array(self.data1)[na_map].tolist()
        y = np.array(self.data2)[na_map].tolist()

        X = sm.add_constant(x)
        reg_formula = sm.OLS(y, X)
        reg_results = reg_formula.fit()

        fitted_col = []
        resid_col = []

        i = 0
        for j in na_map:
            if not j:
                fitted_col.append(reg_results.fittedvalues[i])
                resid_col.append(reg_results.resid[i])
                i += 1
            else:
                fitted_col.append(np.nan)
                resid_col.append(np.nan)

        self.reg_results = reg_results
        self._data['resid'] = resid_col
        self._data['fitted'] = fitted_col

        return reg_results.summary()

    def count(self):
        return len(self.data1.dropna())

    def set_min(self, min_value):
        return self.allow_datapoints_if(lambda d: d >= min_value)

    def set_max(self, max_value):
        return self.allow_datapoints_if(lambda d: d <= max_value)
        pass

    def ban_value(self, values):
        self._data.where(values, inplace=True)
        return self

    def allow_datapoints_if(self, filter_func):
        if self._query_on_column:
            self._data.where((self._data[self._query_column] != self._identifier1 or filter_func(
                self._data[self._measuring_column])), inplace=True)
            self._data.where((self._data[self._query_column] != self._identifier2 or filter_func(
                self._data[self._measuring_column])), inplace=True)
        else:
            self._data.where(filter_func(self._data[self._identifier1]), inplace=True)
            self._data.where(filter_func(self._data[self._identifier2]), inplace=True)

        return self

    def ban_if_column(self, column, filter_func):
        mask = self._data[column].apply(filter_func)
        self._data.loc[mask, :] = np.nan
        return self

    def ban_if_column_value(self, column, banned_values):
        self.ban_if_column(column, lambda b: b in banned_values)
        return self

    def scatterplot(self):
        return sns.scatterplot(x=self.data1, y=self.data2)

    def plot_variance(self):
        print(self.reg_results.fittedvalues.shape)
        print(self.reg_results.resid.shape)

        ax = sns.scatterplot(
            x=self.reg_results.fittedvalues,
            y=self.reg_results.resid,
        )
        ax.set(xlabel="y-hat", ylabel="Residual")

    def plot_residuals(self):
        return sns.histplot(self.reg_results.resid)

    def plot(self):
        if self.reg_results:
            self.scatterplot()
            sns.lineplot(x=self.data1[self.safe_value_map], y=list(self.reg_results.fittedvalues))
        elif self._test_objective == "paired":
            plt.figure(figsize=(8, 4))

            plt.subplot(1, 2, 1)
            sns.scatterplot(data=self._data, x=self._identifier1, y=self._identifier2)
            plt.plot([self.data1.min(), self.data1.max()], [self.data2.min(), self.data2.max()], 'r--')

            plt.subplot(1, 2, 2)
            sns.barplot(data=self._data[[self._identifier1, self._identifier2]], errorbar=None, color=[0.9, 0.9, 0.9])
            sns.lineplot(data=self._data[[self._identifier1, self._identifier2]].T, legend=False, marker='o')
        else:
            sns.kdeplot(data=self._data, x=self._measuring_column, hue=self._query_column, fill=True)
            sns.rugplot(data=self._data, x=self._measuring_column, hue=self._query_column, height=0.1)

            plt.xlabel(self.measuring_var, fontsize=12)
            plt.ylabel("Density", fontsize=12)

        plt.show()

    @property
    def n(self):
        if self._override_n:
            return self._override_n
        elif self.data1:
            return len(self.data1)
        else:
            analysis = TTestPower()
            return analysis.solve_power(effect_size=self.cohens_d, alpha=self._alpha, nobs=None, power=self.power,
                                        alternative=self._tail)

    @n.setter
    def n(self, value):
        self._override_n = value

    @property
    def n2(self):
        if self._override_n2:
            return self._override_n2
        else:
            return len(self.data2)

    @n2.setter
    def n2(self, value):
        self._override_n2 = value

    @property
    def data1(self):
        if self._identifier1:
            return self._get_data(self._identifier1)
        else:
            return None

    @property
    def data2(self):
        if self._identifier1:
            return self._get_data(self._identifier2)
        else:
            return None

    @property
    def hypothesis_summary_str(self):
        if self._tail == "two-sided":
            return "This is a two-sided (non-directional) alternative hypothesis."
        else:
            return "This is a one-sided (directional) alternative hypothesis."

    @property
    def measuring_var(self):
        return self._english_measuring if self._english_measuring is not None else self._measuring_column

    @property
    def average_type(self):
        return "median" if self._test_type == "rank" else "mean"

    @property
    def null_hypothesis(self):
        if self._test_objective == "correlation":
            return f"There is no {self.test_statistic} (the correlation, Pearson's r = 0)"
        else:
            return f"The {self.test_statistic} is zero."

    @property
    def alt_hypothesis(self):
        if self._test_objective == "correlation":
            if self._tail == "greater":
                return f"Those with higher {self._identifier1} have higher {self._identifier2} (the correlation, Pearson's r > 0)"
            elif self._tail == "less":
                return f"Those with higher {self._identifier1} have lower {self._identifier2} (the correlation, Pearson's r < 0)"
            else:
                return f"There is a correlation between {self._identifier1} and {self._identifier2} (the correlation, Pearson's r ≠ 0)"

        return f"The {self.test_statistic} is {self._tail} than zero."

    @property
    def test_statistic(self):
        if self._test_objective == "correlation":
            return f"correlation between {self._identifier1} and {self._identifier2}"
        if self._test_objective == "independent":
            return f"difference in {self.average_type} {self.measuring_var} between group {self._identifier1} and group {self._identifier2}"
        if self._test_objective == "paired":
            return f"{self.average_type} difference in {self.measuring_var} between group {self._identifier1} and group {self._identifier2}"

    def get_conclusion(self, pvalue):
        if pvalue < self._alpha:
            return (f"{self.round(pvalue)} < {self.round(self._alpha)}.\n"
                    f"There is sufficient evidence to reject the null hypothesis.")
        else:
            return (f"{self.round(pvalue)} > {self.round(self._alpha)}.\n"
                    f"There is insufficient evidence to reject the null hypothesis.")

    def get_hypothesis_str(self, results, extra_info="", statistic_is_arr=False, use_df=False):
        statistic = results.statistic[0] if statistic_is_arr else results.statistic
        pvalue = results.pvalue[0] if statistic_is_arr else results.pvalue

        self.p = pvalue

        df_str = ''
        if use_df:
            df = results.df[0] if statistic_is_arr else results.df
            df_str = f'Degrees of freedom: {df}\n'

        return f"""H0: {self.null_hypothesis}
H1: {self.alt_hypothesis}
{self.hypothesis_summary_str}
{df_str}
Test statistic: {self.test_statistic} ({self.round(statistic)})
Alpha: {self._alpha}

P-value: {self.round(pvalue) if pvalue >= 0.001 else '<0.001'} {f"({extra_info})" if extra_info else ""}

{self.get_conclusion(pvalue)}
"""

    def _do_test_is_normal(self, column_now):
        identifier = self._identifier1 if column_now == 1 else self._identifier2
        result = stats.shapiro(self.data1 if column_now == 1 else self.data2)

        group_name = f'{self.measuring_var} of group {identifier}'
        if column_now == -1:
            result = stats.shapiro(self.data_diff)
            group_name = f'difference between the {self.measuring_var} of group {self._identifier1} and {self._identifier2}'

        return f"""H0: The {group_name} is normally distributed.
H1: The {group_name} is not normally distributed.

{self.best_fitting_normal(column_now)}

Test statistic: Shapiro-Wilk W ({self.round(result.statistic)})
Alpha: {self._alpha}

P-value: {self.round(result.pvalue)} (using Shapiro-Wilk Test)

{self.get_conclusion(result.pvalue)}\n\n"""

    def test_is_normal(self, column=1):
        if self._test_objective == "paired":
            return self._do_test_is_normal(-1)

        columns = [column] if column != 0 else [1, 2]
        res = ''
        for column_now in columns:
            res += self._do_test_is_normal(column_now)

        return res.strip()

    def rounding_to(self, n):
        self._sigfig = n

    def round(self, value):
        return '{:g}'.format(float('{:.{p}g}'.format(value, p=self._sigfig)))

    def exec(self):
        if self._is_regression_spec:
            return self.apply_regression_formula(f'{self._regression_lhs} ~ {" + ".join(self._regression_rhs)}')
        elif self._test_type == "permutation":
            if self._test_objective == "correlation":
                def correlate(x, y):
                    tmp = np.corrcoef(x, y)
                    c = tmp[0][1]
                    return c

                function = correlate
                permutation_type = "pairings"
            elif self._test_objective == "independent":
                def dMeans(x, y):
                    return np.mean(x) - np.mean(y)

                function = dMeans
                permutation_type = "independent"
            elif self._test_objective == "paired":
                def mDiff(x, y):
                    return np.mean(x - y)

                function = mDiff
                permutation_type = "samples"
            else:
                raise ValueError('Unsupported test type for permutation test: ' + self._test_objective)

            results = stats.permutation_test((self.data1, self.data2), function, permutation_type=permutation_type,
                                             alternative=self._tail, n_resamples=self._permutation_count)
            return self.get_hypothesis_str(results, extra_info=f"after {self._permutation_count} permutations")
        elif self._test_type == "rank":
            if self._test_objective == "correlation":
                test_type = 'Spearman'
                results = stats.spearmanr(self.data1, self.data2, alternative=self._tail)
            elif self._test_objective == "independent":
                test_type = 'Mann Whiney U'
                results = stats.mannwhitneyu(self.data1, self.data2, alternative=self._tail)
            elif self._test_objective == "paired":
                test_type = 'Wilcoxon'
                results = stats.wilcoxon(self.data1, self.data2, alternative=self._tail)
            else:
                raise ValueError('Unsupported test type for permutation test: ' + self._test_objective)

            return self.get_hypothesis_str(results, extra_info=f"using {test_type} test")
        elif self._test_type == "t-test":
            if self._test_objective == "independent":
                results = stats.ttest_ind(self.data1, self.data2, alternative=self._tail)
            elif self._test_objective == "paired":
                results = stats.ttest_rel(self.data1, self.data2, alternative=self._tail)
            elif self._test_objective == "correlation":
                results = stats.pearsonr(self.data1, self.data2, alternative=self._tail)
            else:
                raise ValueError('Unsupported test type for t-test: ' + self._test_objective)

            self._override_t = results.statistic

            return self.get_hypothesis_str(results, extra_info=f"using t-test", use_df=True)

    @property
    def t(self):
        if self._override_t:
            return self._override_t
        elif self.data1 and self.data2:
            self.exec()
            return self._override_t

    @t.setter
    def t(self, t):
        self._override_t = t

    def using_correlation(self):
        self._test_objective = "correlation"
        return self

    def using_t_test(self):
        self._test_type = "t-test"
        return self

    def t_test_on_one(self, value):
        results = stats.ttest_1samp(self.data1, value, alternative=self._tail)
        return self.get_hypothesis_str(results, extra_info=f"using t-test", statistic_is_arr=True)

    def query_on_column(self, column):
        self._query_on_column = True
        self._query_column = column

        return self

    def datapoint(self, identifier1):
        self._identifier1 = identifier1
        return self

    def is_greater_than(self, identifier2=None):
        self._identifier2 = identifier2
        self._tail = "greater"
        return self

    def is_less_than(self, identifier2=None):
        self._identifier2 = identifier2
        self._tail = "less"
        return self

    def measuring_column(self, column):
        self._measuring_column = column
        return self

    @property
    def data_diff(self):
        if self._test_objective == "paired":
            return self._data["Difference"]

        return None

    def best_fitting_normal(self, column=1):
        if self._test_objective == "paired" and column == 0:
            return f'Best fitting normal for differences: μ={self.round(self.data_diff.mean())}, σ={self.round(self.data_diff.std())}\n'

        res = ''
        if column != 2:
            res += f'Best fitting normal ({self._identifier1}): μ={self.round(self.data1.mean())}, σ={self.round(self.data1.std())}\n'

        if self.data2 is not None and column != 1:
            res += f'Best fitting normal ({self._identifier2}): μ={self.round(self.data2.mean())}, σ={self.round(self.data2.std())}'

        return res.strip()

    def set_datapoints(self, identifier1, identifier2):
        self._identifier1 = identifier1
        self._identifier2 = identifier2
        self._tail = "two-sided"

        return self

    @property
    def cohens_d(self):
        if self._override_cohens_d:
            return self._override_cohens_d
        elif self.data1 and self.data2:
            if self._test_objective == 'correlation':
                r = stats.pearsonr(self.data1, self.data2, alternative=self._tail).statistic
                t = (r * (len(self.data1) - 2) ** 0.5) / ((1 - r ** 2) ** 0.5)
                d = t / (len(self.data1) ** 0.5)

                return d
            else:
                xP = self.data1.mean()
                xG = self.data2.mean()

                sP = self.data1.std()
                sG = self.data2.std()

                nP = self.data1.count()
                nG = self.data2.count()

                s = (((nP - 1) * (sP ** 2) + (nG - 1) * (sG ** 2)) / (nP + nG - 2)) ** 0.5
                return (xG - xP) / s
        elif self.t and self.n:
            return Utilities.t_to_d(self.t, self.n)

    @cohens_d.setter
    def cohens_d(self, x):
        self._override_cohens_d = x

    @property
    def power(self):
        if self._override_power:
            return self._override_power

        if self._test_objective == 'correlation':
            analysis = TTestPower()
            return analysis.solve_power(effect_size=self.cohens_d, alpha=self._alpha, nobs=self.n, power=None,
                                        alternative=self._tail)
        if self._test_objective == 'paired':
            analysis = TTestPower()
            return analysis.solve_power(effect_size=self.cohens_d, alpha=self._alpha, nobs=self.n, power=None,
                                        alternative=self._tail)
        if self._test_objective == 'independent':
            analysis = TTestIndPower()
            return analysis.solve_power(effect_size=self.cohens_d, alpha=self._alpha, nobs1=self.n,
                                        ratio=self.n2 / self.n, power=None, alternative=self._tail)

    @power.setter
    def power(self, power):
        self._override_power = power
