# TODO:版权、名字

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", name="neo4j", password="/")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, task, user_input_devices):
        final_answers = []
        # for sql_ in sqls:
        #     quetion_type = sql_['question_type']
        #     queries = sql_['sql']
        #     answers = []
        #     for query in queries:
        #         ress = self.g.run(query).data()
        #         answers += ress
        #     # print(answers)
        #     final_answer = self.answer_prettify(quetion_type, answers)
        #     if final_answer:
        #         final_answers.append(final_answer)
        #         # print("查询到资料")
        query_app = "MATCH (a:Application)-[:BELONG_TO]->(t:Task) where t.taskID = '{0}' RETURN a.applicationID".format(task)
        ress = self.g.run(query_app).data()
        app_list = [tp['a.applicationID'] for tp in ress]
        app_rank_dict = {}
        # print(len(app_list))
        app_names = dict()
        for app in app_list:
            query_robot = "MATCH (a:Application)-[:APPLY_TO]->(r:Robot) where a.applicationID = '{0}' RETURN a.applicationName, r.robotID".format(app)
            # print(query_device)
            robot = self.g.run(query_robot).data()
            robot_id = robot[0]['r.robotID']
            app_name = robot[0]['a.applicationName']
            app_names[app] = app_name

            query_device = "MATCH (r:Robot)-[:INCLUDES_DEVICE]->(d:Device) where r.robotID = '{0}' RETURN d.deviceID".format(robot_id)
            # print(query_device)
            device = self.g.run(query_device).data()
            device_list = [d['d.deviceID'] for d in device]
            # print(device_list)
            count = 0
            for d in device_list:
                if d in user_input_devices:
                    count += 1

            max_num = max(len(device_list), len(user_input_devices))
            score = count*1.0/max_num


            app_rank_dict[app] = score

        app_sorted_dict = sorted(app_rank_dict.items(), key=lambda x: (x[1], x[0]), reverse=True)


        print(app_sorted_dict)

        for i in range(min(3, len(app_sorted_dict))):
            print(app_sorted_dict[i][1], " : ", app_names[app_sorted_dict[i][0]])


        return final_answers

    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'robot_package':
            desc = [i['package.package_name'] for i in answers]
            subject = answers[0]['r.robot_name']
            final_answer = 'The Robot:{0} has packages: {1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'package_task':
            desc = [i['package.package_name'] for i in answers]
            subject = answers[0]['t.task_name']
            final_answer = 'The {0}-related packages include: {1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))


        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
    # searcher.search_main(1, ['7','9','1'])
    searcher.search_main(1, ['25', '34', '35'])



# use turtlebot2 with rplidar do mapping in simulated environment

