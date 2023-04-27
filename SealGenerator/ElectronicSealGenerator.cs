using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Drawing.Text;
using SealGenerator.Models;

namespace SealGenerator
{
    public class ElectronicSealGenerator
    {
        private const int DEFAULT_COMPANY_NAME_LENGTH = 14;
        private const int DEFAULT_USAGE_NAME_LENGTH = 8;
        private const int DEFAULT_NUMBER_LENGTH = 14;

        private const int MIN_FONT_SIZE = 9;

        public Bitmap CreateSeal(CirleElectronicSealOptions options)
        {
            Font font1 = new Font("思源宋体", 16, FontStyle.Regular, GraphicsUnit.Pixel);
            Font font2 = new Font("思源宋体", 11, FontStyle.Regular, GraphicsUnit.Pixel);
            Font font3 = new Font("思源宋体", 9, FontStyle.Regular, GraphicsUnit.Pixel);
            if (options.SealSize == 0) options.SealSize = 250;
            Bitmap bitmap = new Bitmap(options.SealSize + 30, options.SealSize + 30, PixelFormat.Format32bppArgb);
            Graphics g = Graphics.FromImage(bitmap);
            g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit; ;
            // 绘制电子签章 
            RectangleF rect = new RectangleF(15, 15, options.SealSize, options.SealSize);
            DrawSeal(g, rect, options.CompanyName, options.UsageName, options.SealNumber, font1, font2, font3, options.ShowStar);
            return bitmap;
        }

        public void CreateSeal(CirleElectronicSealOptions options, string filePath)
        {
            var bitmap = CreateSeal(options);
            bitmap.Save(filePath);
        }

        public void CreateSeal(CirleElectronicSealOptions options, Graphics graphics)
        {
            Font font1 = new Font("思源宋体", 16, FontStyle.Regular, GraphicsUnit.Pixel);
            Font font2 = new Font("思源宋体", 11, FontStyle.Regular, GraphicsUnit.Pixel);
            Font font3 = new Font("思源宋体", 9, FontStyle.Regular, GraphicsUnit.Pixel);
            if (options.SealSize == 0) options.SealSize = 250;
            graphics.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;
            // 绘制电子签章
            var x = graphics.VisibleClipBounds.Width * options.Position.PercentageX - options.SealSize / 2;
            var y = graphics.VisibleClipBounds.Height * options.Position.PercentageY - options.SealSize / 2;
            RectangleF rect = new RectangleF(x, y, options.SealSize, options.SealSize);
            DrawSeal(graphics, rect, options.CompanyName, options.UsageName, options.SealNumber, font1, font2, font3, options.ShowStar); ;
        }

        private void DrawSeal(Graphics g, RectangleF rect, string text1, string text2, string text3, Font font1, Font font2, Font font3, bool showStar)
        {
            text1 = text1.Replace("（", "(").Replace("）", ")");
            text2 = text2.Replace("（", "(").Replace("）", ")");

            // 设置绘图属性
            Pen pen = new Pen(Color.Red, 3.0f);
            SolidBrush brush = new SolidBrush(Color.Red);
            StringFormat format = new StringFormat();
            format.Alignment = StringAlignment.Center;
            format.LineAlignment = StringAlignment.Center;

            // 绘制圆形边框 
            g.DrawEllipse(pen, rect);
           

            // 绘制五角星 
            if (showStar)
            {
                var Radius = rect.Width / 2 * 0.45;
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
            }


            float radius = rect.Width / 2.0f - 15.0f;

            // 印章上部分为 PI * 5 / 3，即：300度
            // 两侧各减去10度，避免与中间的部分重叠，即 280 度
            if (!string.IsNullOrEmpty(text1))
            {
                PointF center = new PointF(rect.X + rect.Width / 2.0f, rect.Y + rect.Height / 2.0f);
                float fontSize1 = GetFontSizeToFit(g, text1, font1, radius * 2.0f / 3.0f, DEFAULT_COMPANY_NAME_LENGTH);
                //float fontSize1 = ScaleFontSizeByContainerSize(g, text1, font1, new SizeF(radius * 2.0f / 3.0f, radius * 2.0f / 3.0f));
                Font fontToFit1 = new Font(font1.FontFamily, fontSize1, FontStyle.Bold, GraphicsUnit.Pixel);
                var totalAngle = Math.PI * 5 / 3 - 20 * Math.PI / 180;
                var stepAngle = totalAngle / (text1.Length + 1);
                var startAngle = Math.PI * 4 / 3 - 10 * Math.PI / 180;
                for (int i = 0; i < text1.Length; i++)
                {
                    float angle = (float)(startAngle - (i + 1) * stepAngle);
                    if (angle < 0) angle += (float)Math.PI * 2;
                    PointF point = new PointF(center.X + radius * (float)Math.Cos(angle), center.Y - radius * (float)Math.Sin(angle));
                    g.TranslateTransform(point.X, point.Y);
                    var transformAngle = (float)(angle * 180 / Math.PI + 90);
                    if (transformAngle > 360) transformAngle -= 360;
                    // 注意：RotateTransform() 方法旋转方向时顺时针，所以，要用 360 度减去当前角度
                    // 印章上方的文字需要正对着外侧，所以，要再加上 180 度
                    transformAngle = 360 - transformAngle + 180;
                    g.RotateTransform(transformAngle);
                    g.DrawString(text1[i].ToString(), fontToFit1, brush, 0, 0, format);
                    g.ResetTransform();
                }
            }

            // 绘制印章用途文字
            // 如果该区域宽度为整个区域的70%，则可根据勾股定理计算出对应的纵坐标
            // 且这个纵坐标需要减去文字本身的高度
            if (!string.IsNullOrEmpty(text2))
            {
                var textPosY = rect.Y + radius + Math.Sqrt(Math.Pow(radius, 2) + Math.Pow(0.4, 2)) - 0.1f * rect.Height;
                RectangleF textRect = new RectangleF(rect.X + 0.1f * rect.Width, (float)textPosY, 0.8f * rect.Width, 0.1f * rect.Height);
                float fontSize2 = ScaleFontSizeByContainerSize(g, text2, font2, new SizeF(textRect.Width, textRect.Height));
                Font fontToFit2 = new Font(font2.FontFamily, fontSize2, FontStyle.Bold, GraphicsUnit.Pixel);
                g.DrawString(text2, fontToFit2, brush, textRect, format);
            }


            // 绘制印章编号，占据整个圆的6/1,即 PI * 1 / 3
            // 从 -PI * 2 / 3 开始顺时针为正
            // 两侧各增加 5 度，即 10度
            if (!string.IsNullOrEmpty(text3))
            {
                var center = new PointF(rect.X + rect.Width / 2.0f, rect.Y + rect.Height / 2.0f);
                float fontSize3 = GetFontSizeToFit(g, text1, font3, radius * 2.0f / 3.0f, DEFAULT_NUMBER_LENGTH);
                //float fontSize3 = ScaleFontSizeByContainerSize(g, text1, font3, new SizeF(radius * 2.0f / 3.0f, radius * 2.0f / 3.0f));
                Font fontToFit3 = new Font(font1.FontFamily, fontSize3, FontStyle.Bold, GraphicsUnit.Pixel);
                var totalAngle = Math.PI * 1 / 3 + 10 * Math.PI / 180;
                var stepAngle = totalAngle / (text3.Length + 1);
                var startAngle = -Math.PI * 2 / 3 - 5 * Math.PI / 180;
                for (int i = 0; i < text3.Length; i++)
                {
                    float angle = (float)(startAngle + (i + 1) * stepAngle);
                    if (angle < 0) angle += (float)Math.PI * 2;
                    PointF point = new PointF(center.X + radius * (float)Math.Cos(angle), center.Y - radius * (float)Math.Sin(angle));
                    g.TranslateTransform(point.X, point.Y);
                    var transformAngle = (float)(angle * 180 / Math.PI + 90);
                    if (transformAngle > 360) transformAngle -= 360;
                    transformAngle = 360 - transformAngle;
                    g.RotateTransform(transformAngle);
                    g.DrawString(text3[i].ToString(), fontToFit3, brush, 0, 0, format);
                    g.ResetTransform();
                }
            }

        }

        private float GetFontSizeToFit(Graphics g, string text, Font font, float width, int default_length)
        {
            float fontSize = font.Size;
            if (text.Length > default_length)
            {
                while (g.MeasureString(text, new Font(font.FontFamily, fontSize)).Width > width)
                {
                    fontSize -= 0.5f;
                }
            }

            while (g.MeasureString(text, new Font(font.FontFamily, fontSize)).Width < width)
            {
                fontSize += 0.5f;
            }
            return fontSize;
        }

        private float GetFontSizeToFit(Graphics g, string text, Font font, float width, float height, int default_length)
        {
            float fontSize = font.Size;
            if (text.Length > default_length)
            {
                while (g.MeasureString(text, new Font(font.FontFamily, fontSize)).Width > width)
                {
                    fontSize -= 0.5f;
                }
            }

            // 对字体放大时需要考虑高度的问题
            var measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            while (measuredSize.Width < width && measuredSize.Height < height)
            {
                fontSize += 0.5f;
                measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            }
            return fontSize;
        }

        public static Font GetAdjustedFont(Graphics graphic, string str, Font originalFont, Size containerSize)
        {
            // We utilize MeasureString which we get via a control instance          
            for (int adjustedSize = (int)originalFont.Size; adjustedSize >= 1; adjustedSize--)
            {
                var testFont = new Font(originalFont.Name, adjustedSize, originalFont.Style, GraphicsUnit.Pixel);

                // Test the string with the new size
                var adjustedSizeNew = graphic.MeasureString(str, testFont, containerSize.Width);

                if (containerSize.Height > Convert.ToInt32(adjustedSizeNew.Height))
                {
                    // Good font, return it
                    return testFont;
                }
            }

            return new Font(originalFont.Name, 1, originalFont.Style, GraphicsUnit.Pixel);
        }

        public static float ScaleFontSizeByContainerSize(Graphics g, string text, Font font, SizeF size)
        {
            var fontSize = font.Size;

            // 对字体缩小时需要考虑最小的字体大小
            var measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            while (measuredSize.Width > size.Width)
            {
                fontSize -= 0.5f;
                if (fontSize <= MIN_FONT_SIZE) break;
                measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            }

            // 对字体放大时需要考虑高度的问题
            measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            while (measuredSize.Width < size.Width && measuredSize.Height < size.Height)
            {
                fontSize += 0.5f;
                measuredSize = g.MeasureString(text, new Font(font.FontFamily, fontSize));
            }

            return fontSize;
        }
    }
}
