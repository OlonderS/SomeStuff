using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;
using System.Text;

namespace DDD.CarRental.Core.DomainModelLayer.Policies
{

    public class StandardDiscountPolicy: IDiscountPolicy
    {
        public string Name { get; protected set; }

        public int FreeHours { get; protected set; }

        public StandardDiscountPolicy(int freeHours)
        {
            Name = "Standard discount policy";
            FreeHours = freeHours; 
        }

        public (Money, int) CalculateDiscount(Money total, int numOfHours, Money unitPrice)
        {
            int timeInHours = numOfHours + FreeHours;
            Money discount = unitPrice.MultiplyBy(FreeHours);
            FreeHours = (FreeHours > timeInHours) ? (FreeHours - timeInHours) : 0;
            FreeHours += (int)(numOfHours * 0.1);

            return (discount, FreeHours); //free hours konkretnego kierowcy poprawic


            //FreeHours += (int)(numOfHours / 10);
            //Money discount = unitPrice.MultiplyBy(FreeHours);
            //return discount; //free hours konkretnego kierowcy poprawic
        }
    }
}
