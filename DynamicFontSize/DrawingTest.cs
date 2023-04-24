using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Drawing.Text;

namespace DynamicFontSize;

[TestClass]
public class DrawingTest
{
    private const int MIN_FONT_SIZE = 8;
    private const int MAX_FONT_SIZE = 32;

    [TestMethod]
    [DataRow(250,80,"�������ƣ��������ģ���Ϊ���ʣ���������")]
    [DataRow(250, 80, "֦�����വ���٣����ĺδ��޷���")]
    [DataRow(250, 80, "�ϳ���������")]
    public void Test_DynamicFontSize(int width, int height, string text)
    {
        Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format32bppArgb);
        Graphics g = Graphics.FromImage(bitmap);
        g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit; ;

        //// ����Բ��
        //var center = new Point(width / 2, height / 2);
        //var radius = width / 2 * 0.6f;
        //var rect = new RectangleF(center.X - radius, center.Y - radius, radius * 2, radius * 2);
        var pen = new Pen(Color.Red, 1.5f);
        //g.DrawEllipse(pen, rect);

        g.DrawRectangle(new Pen(Color.Black, 1.5f), new RectangleF(0, 0,width- 1, height-1));

        // ���ƾ���
        //var textPosX = center.X - radius * 0.75f;
        //var textHeight = Math.Sqrt(Math.Pow(radius, 2) - Math.Pow(radius * 0.75f, 2));
        //var textPosY = center.Y - textHeight;
        var textRect = new RectangleF(10f, 30f, width - 20, height - 60);
        g.DrawRectangle(pen, textRect);

        // ��������
        var font = new Font("����", 16);
        var fontSize = ScaleFontSizeByContainerSize(g, text, font, new SizeF(textRect.Width, textRect.Height));
        g.DrawString(text, new Font("����", fontSize), new SolidBrush(Color.Black), textRect);

        //// ���ƻ�������
        //float fontSize1 = ScaleFontSizeByPerimeter(g, text, font, radius, 360);
        //Font fontToFit1 = new Font("����", fontSize1, FontStyle.Bold, GraphicsUnit.Pixel);
        //var totalAngle = Math.PI * 4 / 3;
        //var stepAngle = totalAngle / (text.Length + 1);
        //var startAngle = -Math.PI * 5 / 6;
        //for (int i = 0; i < text.Length; i++)
        //{
        //    float angle = (float)(startAngle - (i + 1) * stepAngle);
        //    if (angle < 0) angle += (float)Math.PI * 2;
        //    PointF point = new PointF(center.X + (radius + 10) * (float)Math.Cos(angle), center.Y - (radius + 10) * (float)Math.Sin(angle));
        //    g.TranslateTransform(point.X, point.Y);
        //    var transformAngle = (float)(angle * 180 / Math.PI + 90);
        //    if (transformAngle > 360) transformAngle -= 360;
        //    // ע�⣺RotateTransform() ������ת����ʱ˳ʱ�룬���ԣ�Ҫ�� 360 �ȼ�ȥ��ǰ�Ƕ�
        //    // ӡ���Ϸ���������Ҫ��������࣬���ԣ�Ҫ�ټ��� 180 ��
        //    transformAngle = 360 - transformAngle + 180;
        //    g.RotateTransform(transformAngle);
        //    g.DrawString(text[i].ToString(), fontToFit1, new SolidBrush(Color.Black), 0, 0);
        //    g.ResetTransform();
        //}

        g.DrawString($"��ǰ�����С={fontSize}", new Font("����", 13), new SolidBrush(Color.Black), new PointF(0, 0));

        bitmap.Save($"{width}_{height}_{text}.png");
    }

    [TestMethod]
    [DataRow(450, 300, "�����ǹ�������Ӱ��ˣ��̳и����ȱ��Ĺ��ٴ�ͳ�������������")]
    [DataRow(450, 300, "�����ǹ�������Ӱ��ˣ��̳и����ȱ��Ĺ��ٴ�ͳ")]
    [DataRow(450, 300, "�����ǹ�������Ӱ���")]
    public void Test_TextWithllipse(int width, int height, string text)
    {
        Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format32bppArgb);
        Graphics g = Graphics.FromImage(bitmap);
        g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit; ;
        g.Clear(Color.White);

        // ������Բ
        var center = new Point(width / 2, height / 2);
        var a = width * 0.5f;
        var b = height * 0.5f;
        var rect = new RectangleF(center.X - a, center.Y - b, 2 * a, 2 * b);
        var pen = new Pen(Color.Red, 3.0f);
        g.DrawEllipse(pen, rect);

        var Radius = rect.Height / 2 * 0.45;
        var Center = new PointF(rect.X + rect.Width / 2, rect.Y + rect.Height / 2);
        PointF[] points = new PointF[]
        {
                    new PointF(Center.X, (float)(Center.Y - Radius)),
                    new PointF((float)(Center.X + Radius * Math.Sin(72 * Math.PI / 180)), (float)(Center.Y - Radius * Math.Cos(72 * Math.PI / 180))),
                    new PointF((float)(Center.X + Radius * Math.Sin(36 * Math.PI / 180)), (float)(Center.Y + Radius * Math.Cos(36* Math.PI / 180))),
                    new PointF((float)(Center.X - Radius * Math.Sin(36 * Math.PI / 180)),(float)( Center.Y + Radius * Math.Cos(36 * Math.PI / 180))),
                    new PointF((float)(Center.X - Radius * Math.Sin(72 * Math.PI / 180)), (float)(Center.Y - Radius * Math.Cos(72 * Math.PI / 180))),
        };

        GraphicsPath path = new GraphicsPath(FillMode.Winding);
        path.AddLine(points[0], points[2]);
        path.AddLine(points[2], points[4]);
        path.AddLine(points[4], points[1]);
        path.AddLine(points[1], points[3]);
        path.AddLine(points[3], points[0]);
        path.CloseFigure();

        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.RotateTransform(0);
        g.FillPath(new SolidBrush(Color.Red), path);


        // ������Բ����
        var font = new Font("����", 16);
        float fontSize1 = ScaleFontSizeByPerimeter(g, text, font, a * 0.9f, b * 0.9f, 360);
        Font fontToFit1 = new Font("����", fontSize1, FontStyle.Bold, GraphicsUnit.Pixel);
        var totalAngle = Math.PI * 4 / 3;
        var stepAngle = totalAngle / (text.Length + 1);
        var startAngle = - Math.PI * 5 / 6;
        for (int i = 0; i < text.Length; i++)
        {
            float angle = (float)(startAngle - (i + 1) * stepAngle);
            if (angle < 0) angle += (float)Math.PI * 2;
            var x = center.X + a * 0.9f * (float)Math.Cos(angle);
            var y = center.Y - b * 0.9f * (float)Math.Sin(angle);
            PointF point = new PointF(x, y);
            g.TranslateTransform(point.X, point.Y);
            var transformAngle = (float)(angle * 180 / Math.PI + 90);
            if (transformAngle > 360) transformAngle -= 360;
            // ע�⣺RotateTransform() ������ת����ʱ˳ʱ�룬���ԣ�Ҫ�� 360 �ȼ�ȥ��ǰ�Ƕ�
            // ӡ���Ϸ���������Ҫ��������࣬���ԣ�Ҫ�ټ��� 180 ��
            transformAngle = 360 - transformAngle + 180;
            g.RotateTransform(transformAngle);
            g.DrawString(text[i].ToString(), fontToFit1, new SolidBrush(Color.Red), 0, 0);
            g.ResetTransform();
        }

        g.DrawString($"��ǰ�����С={fontSize1}", new Font("����", 10), new SolidBrush(Color.Black), new PointF(0, 0));

        bitmap.Save($"{width}_{height}_{text}_��Բ.png");

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
            fontSize -= 0.1f;
            if (fontSize <= MIN_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        // ������Ŵ�ʱ��Ҫ���Ǹ߶ȵ�����
        measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width < perimeter)
        {
            fontSize += 0.1f;
            if (fontSize >= MAX_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        return fontSize;
    }

    static float ScaleFontSizeByPerimeter(Graphics g, string text, Font font,float a, float b, float angle)
    {
        var fontSize = font.Size;

        var h = Math.Pow((a - b) / (a + b), 2);
        var c = Math.PI * (a + b) * (1 + (3 * h / (10 + (4 - 3 * h))));
        var perimeter = c * angle / 360;

        // ��������Сʱ��Ҫ������С�������С
        var measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width > perimeter)
        {
            fontSize -= 0.1f;
            if (fontSize <= MIN_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        // ������Ŵ�ʱ��Ҫ���Ǹ߶ȵ�����
        measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        while (measuredSize.Width < perimeter)
        {
            fontSize += 0.1f;
            if (fontSize >= MAX_FONT_SIZE) break;
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
        }

        return fontSize;
    }
}