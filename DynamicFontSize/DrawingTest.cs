using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Text;

namespace DynamicFontSize;

[TestClass]
public class DrawingTest
{
    private const int MIN_FONT_SIZE = 8;

    [TestMethod]
    [DataRow(200,200,"�����ǹ�������Ӱ��ˣ��̳и����ȱ��Ĺ��ٴ�ͳ�������������")]
    [DataRow(300, 300, "�����ǹ�������Ӱ��ˣ��̳и����ȱ��Ĺ��ٴ�ͳ�������������")]
    [DataRow(400, 400, "�����ǹ�������Ӱ��ˣ��̳и����ȱ��Ĺ��ٴ�ͳ�������������")]
    [DataRow(500, 500, "�����ǹ�������Ӱ���")]
    public void Test_DynamicFontSize(int width, int height, string text)
    {
        Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format32bppArgb);
        Graphics g = Graphics.FromImage(bitmap);
        g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit; ;

        var center = new Point(width / 2, height / 2);
        var radius = width / 2 * 0.6f;
        var rect = new RectangleF(center.X - radius, center.Y - radius, radius * 2, radius * 2);
        var pen = new Pen(Color.Red, 1.50f);
        g.DrawEllipse(pen, rect);

        var textPosX = center.X - radius * 0.75f;
        var textHeight = Math.Sqrt(Math.Pow(radius, 2) - Math.Pow(radius * 0.75f, 2));
        var textPosY = center.Y - textHeight;
        var textRect = new RectangleF(textPosX, (float)textPosY, radius * 0.75f * 2f, (float)textHeight * 2f);
        g.DrawRectangle(pen, textRect);

        var font = new Font("����", 16);
        var fontSize = ScaleFontSizeByContainerSize(g, text, font, new SizeF(textRect.Width, textRect.Height));
        g.DrawString(text, new Font("����", fontSize), new SolidBrush(Color.Blue), textRect);
        g.DrawString($"{width}x{height},fontSize={fontSize}", new Font("����", fontSize), new SolidBrush(Color.Blue), new PointF(0, 0)); 

        float fontSize1 = ScaleFontSizeByPerimeter(g, text, font, radius + 10, 360);
        Font fontToFit1 = new Font("����", fontSize1, FontStyle.Bold, GraphicsUnit.Pixel);
        var totalAngle = Math.PI * 2;
        var stepAngle = totalAngle / (text.Length + 1);
        var startAngle = 0;
        for (int i = 0; i < text.Length; i++)
        {
            float angle = (float)(startAngle - (i + 1) * stepAngle);
            if (angle < 0) angle += (float)Math.PI * 2;
            PointF point = new PointF(center.X + (radius + 10) * (float)Math.Cos(angle), center.Y - (radius + 10) * (float)Math.Sin(angle));
            g.TranslateTransform(point.X, point.Y);
            var transformAngle = (float)(angle * 180 / Math.PI + 90);
            if (transformAngle > 360) transformAngle -= 360;
            // ע�⣺RotateTransform() ������ת����ʱ˳ʱ�룬���ԣ�Ҫ�� 360 �ȼ�ȥ��ǰ�Ƕ�
            // ӡ���Ϸ���������Ҫ��������࣬���ԣ�Ҫ�ټ��� 180 ��
            transformAngle = 360 - transformAngle + 180;
            g.RotateTransform(transformAngle);
            g.DrawString(text[i].ToString(), fontToFit1, new SolidBrush(Color.Blue), 0, 0);
            g.ResetTransform();
        }

        bitmap.Save($"{width}_{height}_{text}.png");
    }

    static float ScaleFontSizeByContainerSize(Graphics g, string text, Font font, SizeF size)
    {
        var fontSize = font.Size;

        // ��������Сʱ��Ҫ������С�������С
        var measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width > size.Width)
        {
            fontSize -= 0.5f;
            if (fontSize <= MIN_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        // ������Ŵ�ʱ��Ҫ���Ǹ߶ȵ�����
        measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width < size.Width && measuredSize.Height < size.Height)
        {
            fontSize += 0.5f;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        return fontSize;
    }

    static float ScaleFontSizeByPerimeter(Graphics g, string text, Font font, float radius, float angle)
    {
        var fontSize = font.Size;

        var perimeter = angle * Math.PI * radius / 180;

        // ��������Сʱ��Ҫ������С�������С
        var measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width > perimeter)
        {
            fontSize -= 0.5f;
            if (fontSize <= MIN_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        // ������Ŵ�ʱ��Ҫ���Ǹ߶ȵ�����
        measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width < perimeter)
        {
            fontSize += 0.5f;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        return fontSize;
    }
}