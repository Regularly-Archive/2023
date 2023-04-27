using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SealGenerator.Models
{
    internal class EllipseElectronicSealOptions : BaseElectronicSealOptions
    {
        /// <summary>
        /// 印章大小
        /// </summary>
        public SizeF SealSize { get; set; }
    }
}
