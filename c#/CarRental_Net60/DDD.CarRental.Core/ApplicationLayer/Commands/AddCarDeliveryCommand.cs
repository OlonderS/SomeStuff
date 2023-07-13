using DDD.CarRental.Core.DomainModelLayer.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.ApplicationLayer.Commands
{
    public class AddCarDeliveryCommand
    {
        public long RentalId { get; set; }
        public Distance Distance { get; set; }
        public DateTime DateTime { get; set; }
    }
}
