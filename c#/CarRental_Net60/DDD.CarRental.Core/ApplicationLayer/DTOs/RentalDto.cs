using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.ApplicationLayer.DTOs
{
    public class RentalDto
    {
        public long RentalId { get; set; }
        public DateTime Started { get; set; }
        public DateTime? Finished { get; set; }
        public int TimeInHours { get; set; }
        public Money Total { get; set; }
        public long CarId { get; set; }
        public long DriverId { get; set; }
        private IDiscountPolicy _policy;
    }
}
