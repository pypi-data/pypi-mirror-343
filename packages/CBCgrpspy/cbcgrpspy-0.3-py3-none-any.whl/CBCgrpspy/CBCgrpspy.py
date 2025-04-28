import os
import numpy as np
import pandas as pd
from scipy.stats import shapiro, f_oneway, kruskal, levene, chi2_contingency, fisher_exact, anderson, ttest_ind, mannwhitneyu

def monte_carlo_fisher(table, num_permutations=10000, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)

    table = np.asarray(table)
    chi2_obs, _, _, _ = chi2_contingency(table, correction=False)

    rows, cols = [], []
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            count = int(table[i, j])
            rows.extend([i] * count)
            cols.extend([j] * count)
    rows = np.array(rows)
    cols = np.array(cols)

    chi2_perm = []
    for _ in range(num_permutations):
        permuted_cols = np.random.permutation(cols)
        perm_table = np.zeros_like(table, dtype=int)
        for i in range(table.shape[0]):
            for j in range(table.shape[1]):
                perm_table[i, j] = np.sum((rows == i) & (permuted_cols == j))
        chi2, _, _, _ = chi2_contingency(perm_table, correction=False)
        chi2_perm.append(chi2)

    chi2_perm = np.array(chi2_perm)
    p_value = np.mean(chi2_perm >= chi2_obs)

    return chi2_obs, p_value


def twogrps(df, gvar, varlist=None, p_rd=3, skewvar=None, norm_rd=2, sk_rd=2, tabNA="no", cat_rd=0, pnormtest=0.05,
            minfactorlevels=10, ShowStatistic=True, ExtractP=0.05, phomogeneity = 0.05):
    hangshu = len(df) - 1
    df2 = df.copy()
    df[gvar] = df[gvar].astype('category')
    groups = df[gvar].cat.categories
    if len(groups) != 2:
        raise ValueError("Group variable must have exactly 2 levels")

    g1, g2 = groups
    df.replace([np.nan], [None], inplace=True)

    if varlist is None:
        varlist = [col for col in df.columns if col != gvar]
    else:
        missing = set(varlist) - set(df.columns)
        if missing:
            raise ValueError(f"Variables not in dataframe: {missing}")

    table_rows = []
    VarExtract = []

    for var in varlist:
        if (
                df[var].dtype.name in ['category', 'object']
                or len(df[var].dropna().unique()) <= minfactorlevels
        ) or (
                (pd.api.types.is_numeric_dtype(df[var]) and (df[var] % 1 == 0).all())
        ) or (
                var in skewvar
        ):

            cross_tab = pd.crosstab(df[var], df[gvar], margins=True, dropna=(tabNA == "no"))
            total_counts = cross_tab.loc[:, 'All']
            g1_counts = cross_tab[g1]
            g2_counts = cross_tab[g2]

            observed = pd.crosstab(df[var], df[gvar], dropna=(tabNA == "no"))
            if observed.shape[0] == 1:
                p = 1.0
                statistic = None
            else:
                chi2, p_pearson, dof, expected = chi2_contingency(observed, lambda_="pearson")
                n_total = observed.sum().sum()
                is_2x2 = (observed.shape == (2, 2))
                low_cells = (expected < 5).sum()
                total_cells = expected.size
                has_invalid = (expected < 1).any()
                if is_2x2:
                    if (expected < 5).any():
                        if has_invalid:
                            test_name = "Fisher精确检验（存在期望<1）"
                            statistic, p_value = fisher_exact(observed)
                            chi2 = statistic
                            p = p_value
                        else:
                            if n_total >= 40:
                                test_name = "连续性校正卡方检验"
                                statistic, p_value, _, _ = chi2_contingency(observed, correction=True)
                                chi2 = statistic
                                p = p_value
                            else:
                                test_name = "Fisher精确检验（2x2小样本）"
                                statistic, p_value = fisher_exact(observed)
                                chi2 = statistic
                                p = p_value
                    else:
                        test_name = "普通卡方检验"
                        statistic, p_value, _, _ = chi2_contingency(observed, correction=False)
                        chi2 = statistic
                        p = p_value
                else:
                    if (low_cells / total_cells) > 0.2 or ((expected < 5).any() and has_invalid):
                        statistic, p_value = monte_carlo_fisher(observed, num_permutations=10000, random_state=None)
                    else:
                        statistic, p_value, dof, expected = chi2_contingency(observed, correction=False)
                    chi2 = statistic
                    p = p_value

            var_rows = []
            for level in observed.index:
                total_pct = total_counts[level] / total_counts['All'] * 100
                g1_pct = g1_counts[level] / g1_counts.sum() * 100 if g1_counts.sum() != 0 else 0
                g2_pct = g2_counts[level] / g2_counts.sum() * 100 if g2_counts.sum() != 0 else 0

                var_rows.append([
                    f"  {level}",
                    f"{total_counts[level]} ({total_pct:.{cat_rd}f})",
                    f"{g1_counts[level]} ({g1_pct:.{cat_rd}f})",
                    f"{g2_counts[level]} ({g2_pct:.{cat_rd}f})",
                    "",
                    ""
                ])

            p_str = f"< {10 ** -p_rd:.0e}" if p < 10 ** -p_rd else f"{p:.{p_rd}f}"
            header_row = [
                f"{var}, n (%)",
                "", "", "",
                p_str,
                f"{statistic:.3f}" if statistic else "Fisher"
            ]
            table_rows.append(header_row)
            table_rows.extend(var_rows)

            if p < ExtractP:
                VarExtract.append(var)

        else:
            data = df[var].dropna()
            group_data = [df.loc[df[gvar] == g, var].dropna() for g in [g1, g2]]
            if hangshu <= 50:
                group_0 = df2.drop(labels='label', axis=1)[df2['label'] == 0][var]
                group_1 = df2.drop(labels='label', axis=1)[df2['label'] == 1][var]
                _, p_value_a = shapiro(group_0)
                _, p_value_b = shapiro(group_1)
                if (skewvar and var in skewvar) or (p_value_a < pnormtest) or (p_value_b < pnormtest):
                    stats_func = lambda \
                        x: f"{np.median(x):.{sk_rd}f} ({np.percentile(x, 25):.{sk_rd}f}, {np.percentile(x, 75):.{sk_rd}f})"
                    test_stat, p = mannwhitneyu(*group_data)
                else:
                    stats_func = lambda x: f"{np.mean(x):.{norm_rd}f} ± {np.std(x):.{norm_rd}f}"
                    _, levene_p = levene(*group_data)
                    if levene_p > phomogeneity:
                        test_stat, p = ttest_ind(*group_data, equal_var=True)
                    else:
                        test_stat, p = ttest_ind(*group_data, equal_var=False)
                p_str = f"< {10 ** -p_rd:.0e}" if p < 10 ** -p_rd else f"{p:.{p_rd}f}"
                row = [
                    f"{var}, {'Median (IQR)' if (p_value_a < pnormtest) or (p_value_b < pnormtest) else 'Mean ± SD'}",
                    stats_func(data),
                    stats_func(group_data[0]),
                    stats_func(group_data[1]),
                    p_str,
                    f"{test_stat:.3f}"
                ]
            else:
                if (skewvar and var in skewvar) or \
                        (anderson(data)[0] > anderson(data)[1][np.where(anderson(data)[2] == pnormtest * 100)[0][0]]):
                    stats_func = lambda \
                        x: f"{np.median(x):.{sk_rd}f} ({np.percentile(x, 25):.{sk_rd}f}, {np.percentile(x, 75):.{sk_rd}f})"
                    test_stat, p = mannwhitneyu(*group_data)
                else:
                    stats_func = lambda x: f"{np.mean(x):.{norm_rd}f} ± {np.std(x):.{norm_rd}f}"
                    _, levene_p = levene(*group_data)
                    if levene_p > phomogeneity:
                        test_stat, p = ttest_ind(*group_data, equal_var=True)
                    else:
                        test_stat, p = ttest_ind(*group_data, equal_var=False)
                p_str = f"< {10 ** -p_rd:.0e}" if p < 10 ** -p_rd else f"{p:.{p_rd}f}"
                row = [
                    f"{var}, {'Median (IQR)' if (anderson(data)[0] > anderson(data)[1][np.where(anderson(data)[2] == pnormtest * 100)[0][0]]) else 'Mean ± SD'}",
                    stats_func(data),
                    stats_func(group_data[0]),
                    stats_func(group_data[1]),
                    p_str,
                    f"{test_stat:.3f}"
                ]

            table_rows.append(row)

            if p < ExtractP:
                VarExtract.append(var)

    columns = [
        "Variables",
        f"Total (n = {len(df)})",
        f"{g1} (n = {len(df[df[gvar] == g1])})",
        f"{g2} (n = {len(df[df[gvar] == g2])})",
        "P-value",
        "statistic"
    ]

    if not ShowStatistic:
        columns.remove("statistic")
        for row in table_rows:
            del row[-1]

    final_table = pd.DataFrame(table_rows, columns=columns)
    final_table.to_excel("./twogrps.xlsx", index=False)
    print(final_table)
    return final_table.reset_index(drop=True), list(set(VarExtract))


def multigrps(df, gvar, varlist=None, p_rd=3, skewvar=None, norm_rd=2, sk_rd=2, tabNA="no", cat_rd=0, pnormtest=0.05,
              minfactorlevels=10, ShowStatistic=False, ExtractP=0.05):
    VarExtract = []

    df = df.copy()

    df[gvar] = pd.Categorical(df[gvar])
    groups = df[gvar].cat.categories
    if len(groups) < 3:
        raise ValueError("分组变量必须包含至少3个水平")

    df = df.replace([np.nan], [None])

    if varlist is None:
        varlist = [col for col in df.columns if col != gvar]
    else:
        missing = set(varlist) - set(df.columns)
        if missing:
            raise ValueError(f"以下变量不存在: {missing}")

    # if skewvar is not None:
    #     invalid_skew = [var for var in skewvar
    #                     if df[var].dtype.name in ['category', 'object']
    #                     or len(df[var].dropna().unique()) <= minfactorlevels]
        # if invalid_skew:
        #     raise ValueError(f"skewvar包含分类变量: {invalid_skew}")

    result_table = pd.DataFrame()

    for var in varlist:
        if (
                df[var].dtype.name in ['category', 'object']
                or len(df[var].dropna().unique()) <= minfactorlevels
        ) or (
                (pd.api.types.is_numeric_dtype(df[var]) and (df[var] % 1 == 0).all())
        ) or (
                var in skewvar
        ):

            observed_df = pd.crosstab(df[var], df[gvar], dropna=(tabNA == "no"))
            observed = observed_df.values
            total_counts = observed_df.sum(axis=1)
            total_pcts = (total_counts / total_counts.sum() * 100).round(cat_rd)
            group_pcts = observed_df.div(observed_df.sum(axis=0), axis=1) * 100
            chi2, p_pearson, dof, expected = chi2_contingency(observed, lambda_="pearson")
            low_cells = (expected < 5).sum()
            total_cells = expected.size
            has_invalid = (expected < 1).any()
            observed = pd.crosstab(df[var], df[gvar],
                                   dropna=(tabNA == "no")).values

            if (low_cells / total_cells) > 0.2 or ((expected < 5).any() and has_invalid):
                statistic, p_value = monte_carlo_fisher(observed, num_permutations=10000, random_state=None)
            else:
                statistic, p_value, dof, expected = chi2_contingency(observed, correction=False)
            chi2 = statistic
            p = p_value

            header = [f"{var}, n (%)"] + [''] * (len(groups)) + [
                f"< 0.001" if p < 10 ** -p_rd else round(p, p_rd),
                "Fisher" if statistic is None else round(statistic, 3)
            ]

            rows = []
            for idx, category in enumerate(observed_df.index):
                row = [
                    f"  {category}",
                    f"{total_counts.iloc[idx]} ({total_pcts.iloc[idx]:.{cat_rd}f})",
                    *[f"{observed_df.iloc[idx, g]} ({group_pcts.iloc[idx, g]:.{cat_rd}f})"
                      for g in range(len(groups))],
                    "", ""
                ]
                rows.append(row)

            columns = ["Variables", f"Total (n={len(df)})"] + \
                      [f"{g} (n={observed_df[g].sum()})" for g in groups] + \
                      ["p", "statistic"]

            var_df = pd.DataFrame([header] + rows, columns=columns)

            if p < ExtractP:
                VarExtract.append(var)

        else:
            data = df[var].dropna()
            if (skewvar and var in skewvar) or \
                    (anderson(data)[0] > anderson(data)[1][np.where(anderson(data)[2] == pnormtest * 100)[0][0]]):
                med = np.median(data)
                q1 = np.percentile(data, 25)
                q3 = np.percentile(data, 75)

                group_meds = []
                for g in groups:
                    g_data = df[df[gvar] == g][var].dropna()
                    group_meds.append(f"{np.median(g_data):.{sk_rd}f} "
                                      f"({np.percentile(g_data, 25):.{sk_rd}f}, "
                                      f"{np.percentile(g_data, 75):.{sk_rd}f})")

                try:
                    statistic, p = kruskal(*[df[df[gvar] == g][var].dropna() for g in groups])
                except:
                    p = 1.0
                    statistic = 0

                var_row = [
                    f"{var}, Median (IQR)",
                    f"{med:.{sk_rd}f} ({q1:.{sk_rd}f}, {q3:.{sk_rd}f})",
                    *group_meds,
                    f"< 0.001" if p < 10 ** -p_rd else round(p, p_rd),
                    round(statistic, 3)
                ]

            else:
                mean = np.mean(data)
                std = np.std(data)

                group_means = []
                for g in groups:
                    g_data = df[df[gvar] == g][var].dropna()
                    group_means.append(f"{np.mean(g_data):.{norm_rd}f} "
                                       f"\u00B1 {np.std(g_data):.{norm_rd}f}")

                try:
                    f_stat, p = f_oneway(*[df[df[gvar] == g][var].dropna() for g in groups])
                except:
                    p = 1.0
                    f_stat = 0

                var_row = [
                    f"{var}, Mean \u00B1 SD",
                    f"{mean:.{norm_rd}f} \u00B1 {std:.{norm_rd}f}",
                    *group_means,
                    f"< 0.001" if p < 10 ** -p_rd else round(p, p_rd),
                    round(f_stat, 3)
                ]

            var_df = pd.DataFrame([var_row], columns=[
                "Variables",
                f"Total (n={len(df)})",
                *[f"{g} (n={len(df[df[gvar] == g])})" for g in groups],
                "p",
                "statistic"
            ])

            if p < ExtractP:
                VarExtract.append(var)

        result_table = pd.concat([result_table, var_df], ignore_index=True)

    if not ShowStatistic:
        result_table = result_table.drop(columns="statistic", errors="ignore")

    final_columns = ["Variables", f"Total (n={len(df)})"] + \
                    [f"{g} (n={len(df[df[gvar] == g])})" for g in groups] + \
                    (["p", "statistic"] if ShowStatistic else ["p"])

    result_table = result_table[final_columns]
    result_table.to_excel("./multigrps.xlsx", index=False)
    print(result_table)
    return result_table, list(set(VarExtract))


def dataAnalysis(df_path,
                 label_series="label",
                 skewvaranalysis=["None"],
                 norm_rd=2,
                 sk_rd=2,
                 cat_rd=0,
                 pnormtest=0.05,
                 extractp=0.05,
                 phomogeneity=0.05,
                 maxfactorlevels=10,
                 showstatistic=True):
    _, a = os.path.splitext(df_path)
    if a in [".csv", ".CSV"]:
        df = pd.read_csv(df_path)
    elif a in [".xlsx", ".XLXS"]:
        df = pd.read_excel(df_path)
    else:
        raise ValueError("Input csv or xlsx!")
    varlistanalysis = df.drop(columns=label_series, axis=1).columns.tolist()
    p_rd = 3
    tabna = "no"
    if len(df[label_series].unique()) == 2:
        twogrps(df, label_series, varlist=varlistanalysis, p_rd=p_rd, skewvar=skewvaranalysis, norm_rd=norm_rd, sk_rd=sk_rd, tabNA=tabna, cat_rd=cat_rd, pnormtest=pnormtest,
            minfactorlevels=maxfactorlevels, ShowStatistic=showstatistic, ExtractP=extractp, phomogeneity = phomogeneity)
    else:
        multigrps(df, label_series, varlist=varlistanalysis, p_rd=p_rd, skewvar=skewvaranalysis, norm_rd=norm_rd, sk_rd=sk_rd, tabNA=tabna, cat_rd=cat_rd, pnormtest=pnormtest,
            minfactorlevels=maxfactorlevels, ShowStatistic=showstatistic, ExtractP=extractp)