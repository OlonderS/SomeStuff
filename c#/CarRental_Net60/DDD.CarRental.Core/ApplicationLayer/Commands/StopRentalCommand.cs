using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.ApplicationLayer.Commands
{
    public class StopRentalCommand
    {
        public long RentalId { get; set; }
        public int TimeInHours { get; set; }
        public DateTime Finished { get; set; }

    }
}
