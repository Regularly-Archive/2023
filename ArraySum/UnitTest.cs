namespace ArraySuming;
using System;

public class UnitTest
{
    [Theory]
    [InlineData(new int[] { 9, 8, 5, 7 }, new int[] { 2, 8, 9 })]
    [InlineData(new int[] { 1, 8, 5, 7 }, new int[] { 2, 8, 9 })]
    [InlineData(new int[] { 1, 8 }, new int[] { 2, 8 })]
    [InlineData(new int[] { 8 }, new int[] { 8 })]
    public void TestArraySum(int[] m, int[] n)
    {
        var input_m = decimal.Parse(string.Join("", m));
        var input_n = decimal.Parse(string.Join("", n));
        var output = input_m + input_n;
        var expected = output.ToString();

        var actual = string.Join("", ArraySum(m, n));
        Console.WriteLine(actual);
        Assert.Equal(expected, actual);
    }

    public int[] ArraySum(int[] m, int[] n)
    {
        if (m != null && n == null) return m;
        if (n != null && m == null) return n;
        if (m == null && n == null) return null;
        if (m.Length == 0 && n.Length == 0) return new int[] { };


        var i = Math.Max(m.Length, n.Length) - 1;
        var j = Math.Min(m.Length, n.Length) - 1;

        while (i >= 0)
        {
            var sum = j >= 0 ? m[i] + n[j] : m[i];
            if (sum > 10)
            {
                // 处理进位问题
                m[i] = sum % 10;
                if (i >= 1)
                {
                    m[i - 1] += sum / 10;
                }
                else
                {
                    var tmp = new int[m.Length + 1];
                    tmp[0] = sum / 10;
                    m.CopyTo(tmp, 1);
                    m = tmp;
                }
            }
            else
            {
                m[i] = sum;
            }
            i--;
            j--;
        }

        var first = m[0];
        if (first > 10)
        {
            m[0] = first % 10;
            var tmp = new int[m.Length + 1];
            tmp[0] = first / 10;
            m.CopyTo(tmp, 1);
            m = tmp;
        }

        return m;
    }
}