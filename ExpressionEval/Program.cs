using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ExpressionCalculator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Expression Calculator\n");

            // 输入表达式
            Console.WriteLine("请输入表达式：");
            string expression = Console.ReadLine();

            // 计算表达式
            try
            {
                double result = EvaluateExpression(expression);
                Console.WriteLine("计算结果为：" + result);
            }
            catch (Exception ex)
            {
                Console.WriteLine("计算错误：" + ex.Message);
            }

            Console.ReadKey();
        }

        // 计算表达式的主方法
        static double EvaluateExpression(string expression)
        {
            // 转换成后缀表达式
            string[] postfixTokens = ConvertToPostfix(expression);

            // 使用栈计算后缀表达式
            Stack<double> stack = new Stack<double>();
            foreach (string token in postfixTokens)
            {
                if (IsOperand(token))  // 操作数入栈
                {
                    stack.Push(double.Parse(token));
                }
                else  // 运算符计算
                {
                    double operand2 = stack.Pop();
                    double operand1 = stack.Pop();
                    double result = ApplyOperator(token, operand1, operand2);
                    stack.Push(result);
                }
            }

            // 栈中留下的就是最终结果
            return stack.Pop();
        }

        // 转换成后缀表达式
        static string[] ConvertToPostfix(string expression)
        {
            // 定义操作符优先级
            Dictionary<string, int> operatorPrecendence = new Dictionary<string, int>()
            {
                { "(", 0 },
                { "+", 1 },
                { "-", 1 },
                { "*", 2 },
                { "/", 2 },
                { "^", 3 },
            };

            // 分离出各个符号
            string[] tokens = expression.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);

            // 使用栈保存操作符
            List<string> postfix = new List<string>();
            Stack<string> stack = new Stack<string>();

            foreach (string token in tokens)
            {
                if (IsOperand(token))  // 操作数添加到后缀表达式中
                {
                    postfix.Add(token);
                }
                else if (token == "(")  // 左括号入栈
                {
                    stack.Push(token);
                }
                else if (token == ")")  // 右括号出栈直到左括号
                {
                    while (stack.Count > 0 && stack.Peek() != "(")
                    {
                        postfix.Add(stack.Pop());
                    }
                    if (stack.Count == 0 || stack.Pop() != "(")
                    {
                        throw new Exception("缺少左括号");
                    }
                }
                else  // 运算符处理
                {
                    // 弹出优先级大于等于当前运算符的操作符
                    while (stack.Count > 0 && stack.Peek() != "("
                            && operatorPrecendence[stack.Peek()] >= operatorPrecendence[token])
                    {
                        postfix.Add(stack.Pop());
                    }
                    stack.Push(token);
                }
            }

            // 剩余的操作符出栈
            while (stack.Count > 0)
            {
                if (stack.Peek() == "(")
                {
                    throw new Exception("缺少右括号");
                }
                postfix.Add(stack.Pop());
            }

            // 返回后缀表达式
            return postfix.ToArray();
        }

        // 是否是操作数
        static bool IsOperand(string token)
        {
            double number;
            return double.TryParse(token, out number);
        }

        // 应用运算符
        static double ApplyOperator(string op, double operand1, double operand2)
        {
            switch (op)
            {
                case "+":
                    return operand1 + operand2;
                case "-":
                    return operand1 - operand2;
                case "*":
                    return operand1 * operand2;
                case "/":
                    if (operand2 == 0)
                    {
                        throw new Exception("除数不能为零");
                    }
                    return operand1 / operand2;
                case "^":
                    return Math.Pow(operand1, operand2);
                default:
                    throw new Exception("未知的操作符：" + op);
            }
        }
    }
}