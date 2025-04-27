import webclient as zqyhttpclient

myclient = zqyhttpclient.ModelClient(base_url="http://172.30.6.188")  # 初始化client


if __name__ == '__main__':
    try:
        # 获取规则列表
        rules = myclient.list_rules()
        print(f"共有{len(rules)}条规则")
        print(rules)

        # 获取规则协议
        ruleTaskInfo = myclient.get_rule_protocol(rule_id=1911658357835882497)
        print(ruleTaskInfo)

        # 执行规则
        taskId = myclient.execute_rule_protocol(protocol_data=ruleTaskInfo)
        print(taskId)

        # 查询任务结果
        taskInfo = myclient.get_task_info(task_id=taskId)
        print(taskInfo)

    except zqyhttpclient.FinanceAPIError as e:
        print(f"API调用失败: {e} (状态码: {e.status_code})")
        if e.detail:
            print(f"错误详情: {e.detail}")
