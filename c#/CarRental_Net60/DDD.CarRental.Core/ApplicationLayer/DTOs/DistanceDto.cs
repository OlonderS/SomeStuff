using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public class DistanceDto
    {
        public string Car { get; set; }
        public decimal Value { get; set; }
        public UnitDistanceEnum Unit { get; set; }

    }
}
