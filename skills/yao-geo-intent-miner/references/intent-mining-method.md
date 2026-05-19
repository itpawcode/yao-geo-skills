# 意图挖掘方法

## 双层意图

- 任务层：信息型、导航/验证型、交易/行动型。
- GEO 操作层：信息型、推荐型、比较型、交易型、风险型、价格型、替代型、场景型、品牌验证型。

## 五段式查询重写

- `user_question`：保留用户口语问法。
- `standalone_rewrite`：把追问改写成独立问题。
- `retrieval_rewrite`：平台可能检索的短语和专业词。
- `evidence_query`：用于找案例、标准、价格、资质、数据和证明材料。
- `title_seed`：给标题生成和内容生产使用的选题输入。

## 追问链路

每条追问至少包含 `root_question_id`、`parent_question_id`、`follow_up_level`、`context_dependency`、`standalone_rewrite`、`platform_fit` 和 `sample_prompt`。
