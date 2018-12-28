import unittest
from main.sample_api import ProductionClass
from main.sample_api import API
from mock import patch
from mock import Mock,MagicMock
from nose_parameterized import parameterized
# from mock import create_autospec


class SampleTestCase(unittest.TestCase):

    def setUp(self):
        """
            在测试用例执行开始时使用它来执行任务
            例如设置环境或设置全局对象
        """
        print("setUp")
        pass

    def tearDown(self):
        """
        使用它来清除由于执行结束时的测试而创建的数据/对象
        """
        print("tearDown")
        pass

    # CASE 1 : Very Basic Test case
    """该测试用例是测试ProductionClass的方法函数"""
    def test_sample_test_case(self):
        p_class = ProductionClass()
        resp = p_class.method('1')
        self.assertEqual(1,resp)

    # CASE 2 : Without mocking function test case
    def test_resp_messages(self):
        """
        此测试用例测试ProductionClass的get_url_status_message函数。
        此函数检查URL的状态并返回格式消息。可帮助我们更好地了解测试用例失败的原因
        """
        p_class = ProductionClass()
        resp = p_class.get_url_status_message()
        # print(resp)
        print(resp!="ok")
        self.assertTrue(resp!="ok",msg="Expected ooo but got resp = {0}".format(resp))


    # CASE 3: Test case using Mock
    # patch is the decorator from mock, it will mock the object and pass it to the underlying function.
    # It accepts the full path (sys.path) of the object/method to be mocked.
    #patch是mock的装饰器，它会模拟对象并将其传递给底层的函数。
    #它接受要模拟的对象/方法的完整路径（sys.path）。
    @patch('main.sample_api.API.status')
    def test_resp_messages_with_mock(self, g_api_method):
        """
        单元测试用例的目的应该是测试get_url_status_message方法的功能，而不是底层API。
       在这个测试用例中，我们模拟了API类的'status'方法。
       另外，为了测试所有场景，我们为这个模拟方法分配不同的返回值。
        这样我们就不会进行实际的API调用，只是模仿它的行为。
        """
        p_class = ProductionClass()

        g_api_method.return_value = 200
        # when `main.sample_api.API.status` will be called in this context, it will return 200
        resp = p_class.get_url_status_message()
        self.assertEqual(resp,"ok")

        g_api_method.return_value = 302
        # when `main.sample_api.API.status` will be called in this context, it will return 302
        resp = p_class.get_url_status_message()
        self.assertEqual(resp,"redirection")

        g_api_method.return_value = 500
        resp= p_class.get_url_status_message()
        self.assertEqual(resp,"Error")

        g_api_method.return_value = "Error"
        resp= p_class.get_url_status_message()
        self.assertEqual(resp,"Network")

        g_api_method.return_value = None
        resp= p_class.get_url_status_message()
        self.assertEqual(resp,"UNKNOWN")

    # Case 4: Using Parameterized
    @parameterized.expand([
        ("OK", 200,"ok"),
        ("REDIRECT", 302,"redirection"),
        ("ERROR", 500,"Error"),
        ("NETWORK", 'Error',"Network"),
        ("NONE", None, "UNKNOWN"),
    ])
    @patch('main.sample_api.API.status')
    def test_resp_messages_with_parameterised_and_mock(self, name, input_case, expected, g_api_method):
        p_class = ProductionClass()
        g_api_method.return_value = input_case
        resp = p_class.get_url_status_message()
        self.assertEqual(resp, expected)

    # Case 5: Using autospec
    @patch('main.sample_api.API', spec=API) # relative path
    def test_resp_messages_new_auto_spec(self, g_api):
        p_class = ProductionClass()
        # case 1, 200:
        status_fun = MagicMock(return_value=200)
        g_api.status = status_fun
        g_api.status.return_value = 200
        resp = p_class.get_url_status_message()
        self.assertEqual(resp,"UNKNOWN")


    # def test_resp_messages_new_auto_spec_another_way(self):
    #     """
    #     can also use autospec directly
    #     :return:
    #     """
    #     p_class = ProductionClass()
    #     # case 1, 200:
    #     m_method = create_autospec(API.status,return_value=200)
    #     print(m_method)
    #     #g_api.status.return_value = 200
    #     resp = p_class.get_url_status_message()
    #     self.assertEqual(resp,"Network")


    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests(self, r_object, resp_obj):

        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj

        resp_obj.status_code = 200
        p_class = ProductionClass()
        resp_g = p_class.get_status_obj_from_requests("GET")
        self.assertEqual(200,resp_g)

        resp_obj.status_code = 405
        resp_p = p_class.get_status_obj_from_requests("POST")
        self.assertEqual(405,resp_p)

        resp_p = p_class.get_status_obj_from_requests("NONE")
        self.assertEqual(404, resp_p)


    @parameterized.expand([
        ("GET", 200),
        ("POST", 405),
        ("NONE", 404),])
    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests_params(self,call_type, st_code, r_object,resp_obj):
        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj
        resp_obj.status_code = st_code
        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests(call_type)
        self.assertEqual(st_code,resp)

    @parameterized.expand([
        ("GET", 200),
        ("POST", 405),
        ("NONE", 404),
    ])
    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests_side_effect(self, call_type, st_code, r_object, resp_obj):
        """
        在这个测试中，我们故意在mocked函数的side_effect属性中添加`AttributeError`，
        它模拟生产中异常引发的确切行为，因此它也涵盖了代码的异常块。
        """
        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj

        resp_obj.status_code = st_code

        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests_side_effect(call_type)
        self.assertEqual(st_code,resp)

        r_object.get.side_effect = AttributeError()
        r_object.post.side_effect = AttributeError()
        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests_side_effect(call_type)
        self.assertEqual(404,resp)

# if __name__ == "__main__":
#     result_path=os.path.join(report_path,"result.html")
#
#     fp=open(result_path,"wb")
#     runner=HTMLTestRunner_jpg.HTMLTestRunner(stream=fp,title="测试报告",description="用例执行情况")
#     runner.run(all_case())
#     fp.close()
suit=unittest.TestSuite()
with open("report.txt","w")as f:
    runner=unittest.TextTestRunner(stream=f,descriptions="测试报告",verbosity=2)
    runner.run(suit)
