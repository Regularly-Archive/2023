namespace SealGenerator.Models
{
    internal class BaseElectronicSealOptions
    {
        /// <summary>
        /// 公司名称
        /// </summary>
        public string CompanyName { get; set; }

        /// <summary>
        /// 公司名称字符间距
        /// </summary>
        public float CompanyNameSpacing { get; set; }

        /// <summary>
        /// 印章用途
        /// </summary>
        public string UsageName { get; set; }

        /// <summary>
        /// 印章用途字符间距
        /// </summary>
        public float UsageNameSpacing { get; set; }

        /// <summary>
        /// 印章用途高度系数
        /// </summary>
        public float UsageNameHeightFactor { get; set; }

        /// <summary>
        /// 印章编号
        /// </summary>
        public string SealNumber { get; set; }

        /// <summary>
        ///  印章编号字符间距
        /// </summary>
        public float SealNumberSpacing { get; set; }

        /// <summary>
        /// 是否展示五角星，默认展示
        /// </summary>
        public bool ShowStar { get; set; } = true;

        /// <summary>
        /// 五角星放缩系数
        /// </summary>
        public bool StarScalingFactor { get; set; }

        /// <summary>
        /// 印章位置
        /// </summary>
        public SealPosition Position { get; set; }
    }
}
