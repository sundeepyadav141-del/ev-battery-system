import datetime
import math

class EVBatterySystem:
    """
    EV Battery Intelligence System
    Analyzes battery health, predicts range, and optimizes charging
    """
    
    def __init__(self, battery_capacity_kwh, initial_soh=100):
        """
        Initialize the EV Battery System
        battery_capacity_kwh: Total battery capacity in kWh (e.g., 60 for 60kWh battery)
        initial_soh: State of Health percentage (100 = new battery)
        """
        self.battery_capacity = battery_capacity_kwh
        self.soh = initial_soh  # State of Health
        self.current_charge = 100  # Current charge percentage
        
    def calculate_available_capacity(self):
        """Calculate actual available capacity based on battery health"""
        return (self.battery_capacity * self.soh) / 100
    
    def predict_range(self, speed_kmh=60, temperature_c=25, ac_usage=False, 
                     driving_style='normal', terrain='flat'):
        """
        Predict vehicle range based on various conditions
        """
        # Base consumption (kWh per 100km) - typical for mid-size EV
        base_consumption = 15
        
        # Speed impact
        if speed_kmh <= 50:
            speed_factor = 0.85
        elif speed_kmh <= 80:
            speed_factor = 1.0
        elif speed_kmh <= 110:
            speed_factor = 1.25
        else:
            speed_factor = 1.5
        
        # Temperature impact
        if temperature_c < 0:
            temp_factor = 1.4
        elif temperature_c < 10:
            temp_factor = 1.25
        elif temperature_c > 35:
            temp_factor = 1.15
        else:
            temp_factor = 1.0
        
        # AC usage impact
        ac_factor = 1.15 if ac_usage else 1.0
        
        # Driving style impact
        style_factors = {
            'eco': 0.85,
            'normal': 1.0,
            'sport': 1.3
        }
        style_factor = style_factors.get(driving_style, 1.0)
        
        # Terrain impact
        terrain_factors = {
            'flat': 1.0,
            'hilly': 1.2,
            'mountain': 1.4
        }
        terrain_factor = terrain_factors.get(terrain, 1.0)
        
        # Calculate total consumption
        total_consumption = (base_consumption * speed_factor * temp_factor * 
                           ac_factor * style_factor * terrain_factor)
        
        # Calculate range
        available_capacity = self.calculate_available_capacity()
        usable_capacity = (available_capacity * self.current_charge) / 100
        predicted_range = (usable_capacity / total_consumption) * 100
        
        return {
            'range_km': round(predicted_range, 2),
            'consumption_per_100km': round(total_consumption, 2),
            'available_energy_kwh': round(usable_capacity, 2)
        }
    def calculate_charging_time(self, target_charge=100, charger_power_kw=7.4):
        """
        Calculate time needed to charge battery
        charger_power_kw: Charger power (3.7kW home, 7.4kW fast home, 50kW DC fast, 150kW ultra-fast)
        """
        current_energy = (self.calculate_available_capacity() * self.current_charge) / 100
        target_energy = (self.calculate_available_capacity() * target_charge) / 100
        energy_needed = target_energy - current_energy
        
        if energy_needed <= 0:
            return {
                'charging_time_hours': 0,
                'charging_time_minutes': 0,
                'energy_added_kwh': 0,
                'message': 'Battery already at or above target charge'
            }
        
        # Charging efficiency (typically 85-90%)
        efficiency = 0.88
        actual_energy_needed = energy_needed / efficiency
        
        charging_time_hours = actual_energy_needed / charger_power_kw
        charging_time_minutes = charging_time_hours * 60
        
        return {
            'charging_time_hours': round(charging_time_hours, 2),
            'charging_time_minutes': round(charging_time_minutes, 1),
            'energy_added_kwh': round(energy_needed, 2),
            'charger_type': self._get_charger_type(charger_power_kw)
        }
    
    def _get_charger_type(self, power_kw):
        """Identify charger type based on power"""
        if power_kw <= 3.7:
            return "Level 1 (Home - Standard)"
        elif power_kw <= 11:
            return "Level 2 (Home - Fast)"
        elif power_kw <= 60:
            return "DC Fast Charger"
        else:
            return "Ultra-Fast DC Charger"
    
    def calculate_battery_degradation(self, years_used, avg_cycles_per_year=200, 
                                     fast_charge_percentage=30):
        """
        Estimate battery degradation over time
        years_used: How many years the battery has been used
        avg_cycles_per_year: Average charge cycles per year
        fast_charge_percentage: Percentage of fast charging usage
        """
        total_cycles = years_used * avg_cycles_per_year
        
        # Base degradation: 2-3% per year typical
        time_degradation = years_used * 2.5
        
        # Cycle degradation: increases with more cycles
        cycle_degradation = (total_cycles / 1000) * 1.5
        
        # Fast charging impact: additional degradation
        fast_charge_impact = (fast_charge_percentage / 100) * years_used * 1.2
        
        total_degradation = time_degradation + cycle_degradation + fast_charge_impact
        
        # Cap at realistic values
        total_degradation = min(total_degradation, 30)  # Max 30% degradation
        
        new_soh = 100 - total_degradation
        self.soh = max(new_soh, 70)  # Minimum 70% SOH
        
        return {
            'current_soh': round(self.soh, 1),
            'degradation_percentage': round(total_degradation, 1),
            'estimated_remaining_cycles': max(0, 2000 - total_cycles),
            'health_status': self._get_health_status(self.soh)
        }
    
    def _get_health_status(self, soh):
        """Determine battery health status"""
        if soh >= 95:
            return "Excellent"
        elif soh >= 85:
            return "Good"
        elif soh >= 75:
            return "Fair"
        else:
            return "Poor - Consider replacement"
    
    def compare_ev_vs_ice(self, annual_km=15000, petrol_price_per_liter=1.8, 
                         electricity_price_per_kwh=0.15, ice_fuel_efficiency=15):
        """
        Compare EV costs vs Internal Combustion Engine vehicle
        annual_km: Kilometers driven per year
        petrol_price_per_liter: Current petrol price
        electricity_price_per_kwh: Electricity cost
        ice_fuel_efficiency: ICE vehicle fuel efficiency (km per liter)
        """
        # EV costs
        range_data = self.predict_range()
        ev_consumption_per_100km = range_data['consumption_per_100km']
        ev_energy_per_year = (annual_km / 100) * ev_consumption_per_100km
        ev_fuel_cost_per_year = ev_energy_per_year * electricity_price_per_kwh
        
        # ICE costs
        ice_liters_per_year = annual_km / ice_fuel_efficiency
        ice_fuel_cost_per_year = ice_liters_per_year * petrol_price_per_liter
        
        # Savings
        annual_savings = ice_fuel_cost_per_year - ev_fuel_cost_per_year
        monthly_savings = annual_savings / 12
        
        return {
            'ev_annual_cost': round(ev_fuel_cost_per_year, 2),
            'ice_annual_cost': round(ice_fuel_cost_per_year, 2),
            'annual_savings': round(annual_savings, 2),
            'monthly_savings': round(monthly_savings, 2),
            'savings_percentage': round((annual_savings / ice_fuel_cost_per_year) * 100, 1),
            'ev_cost_per_km': round(ev_fuel_cost_per_year / annual_km, 3),
            'ice_cost_per_km': round(ice_fuel_cost_per_year / annual_km, 3)
        }
    
    def optimal_charging_recommendation(self):
        """Provide optimal charging recommendations for battery longevity"""
        recommendations = []
        
        if self.current_charge < 20:
            recommendations.append("⚠️ Charge soon - Low battery can stress cells")
        
        if self.current_charge > 90:
            recommendations.append("✓ Avoid charging to 100% daily - Keep between 20-80% for longevity")
        
        recommendations.append("💡 Ideal daily range: 20% - 80% charge")
        recommendations.append("🔌 Use slow charging when possible - Reduces heat stress")
        recommendations.append("🌡️ Avoid extreme temperatures while charging")
        recommendations.append("⚡ Fast charging: Use only when necessary (<20% of charges)")
        
        return recommendations
    # Main Program - User Interface
def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_section(text):
    """Print formatted section"""
    print(f"\n--- {text} ---")

def display_dict(data, indent=2):
    """Display dictionary in readable format"""
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').title()
        print(" " * indent + f"{formatted_key}: {value}")

def main():
    """Main program execution"""
    print_header("🔋 EV BATTERY INTELLIGENCE SYSTEM 🔋")
    print("      Advanced Battery Management & Range Optimization")
    print("           For Electric Vehicle Analysis")
    
    # Get user input for battery specifications
    print_section("Battery Specifications")
    
    try:
        battery_capacity = float(input("Enter battery capacity (kWh) [e.g., 60]: ") or "60")
        battery_age = float(input("Enter battery age (years) [e.g., 2]: ") or "2")
        current_charge = float(input("Enter current charge level (%) [e.g., 75]: ") or "75")
        
        # Initialize the system
        ev = EVBatterySystem(battery_capacity_kwh=battery_capacity)
        ev.current_charge = current_charge
        
        # Calculate battery degradation
        print_section("Battery Health Analysis")
        cycles_per_year = int(input("Average charge cycles per year [e.g., 200]: ") or "200")
        fast_charge_usage = float(input("Fast charging usage (%) [e.g., 30]: ") or "30")
        
        degradation = ev.calculate_battery_degradation(
            years_used=battery_age,
            avg_cycles_per_year=cycles_per_year,
            fast_charge_percentage=fast_charge_usage
        )
        
        print_header("BATTERY HEALTH REPORT")
        display_dict(degradation)
        print(f"\n  Available Capacity: {ev.calculate_available_capacity():.2f} kWh")
        
        # Range prediction
        print_section("Range Prediction Parameters")
        speed = float(input("Average speed (km/h) [e.g., 80]: ") or "80")
        temperature = float(input("Outside temperature (°C) [e.g., 25]: ") or "25")
        ac_usage = input("AC usage? (yes/no) [no]: ").lower().startswith('y')
        
        print("\nDriving Style Options: eco, normal, sport")
        driving_style = input("Select driving style [normal]: ") or "normal"
        
        print("\nTerrain Options: flat, hilly, mountain")
        terrain = input("Select terrain [flat]: ") or "flat"
        
        range_data = ev.predict_range(
            speed_kmh=speed,
            temperature_c=temperature,
            ac_usage=ac_usage,
            driving_style=driving_style,
            terrain=terrain
        )
        
        print_header("RANGE PREDICTION RESULTS")
        display_dict(range_data)
        
        # Charging time calculation
        print_section("Charging Analysis")
        target_charge = float(input("Target charge level (%) [e.g., 100]: ") or "100")
        
        print("\nCharger Options:")
        print("  1. Home Charger (3.7 kW)")
        print("  2. Fast Home Charger (7.4 kW)")
        print("  3. DC Fast Charger (50 kW)")
        print("  4. Ultra-Fast Charger (150 kW)")
        
        charger_choice = input("Select charger [2]: ") or "2"
        charger_powers = {"1": 3.7, "2": 7.4, "3": 50, "4": 150}
        charger_power = charger_powers.get(charger_choice, 7.4)
        
        charging_data = ev.calculate_charging_time(
            target_charge=target_charge,
            charger_power_kw=charger_power
        )
        
        print_header("CHARGING TIME ESTIMATION")
        display_dict(charging_data)
        
        # Cost comparison
        print_section("Cost Analysis Parameters")
        annual_km = float(input("Annual kilometers driven [e.g., 15000]: ") or "15000")
        petrol_price = float(input("Petrol price per liter (₹) [e.g., 110]: ") or "110")
        electricity_price = float(input("Electricity price per kWh (₹) [e.g., 8]: ") or "8")
        ice_efficiency = float(input("ICE vehicle efficiency (km/L) [e.g., 15]: ") or "15")
        
        # Convert rupees to standard units (using factor for calculation)
        petrol_price_calc = petrol_price / 100  # Normalized
        electricity_price_calc = electricity_price / 100  # Normalized
        
        cost_comparison = ev.compare_ev_vs_ice(
            annual_km=annual_km,
            petrol_price_per_liter=petrol_price_calc,
            electricity_price_per_kwh=electricity_price_calc,
            ice_fuel_efficiency=ice_efficiency
        )
        
        print_header("EV vs ICE COST COMPARISON (Annual)")
        
        # Adjust display values back to rupees
        print(f"  EV Annual Cost: ₹{cost_comparison['ev_annual_cost'] * 100:.2f}")
        print(f"  ICE Annual Cost: ₹{cost_comparison['ice_annual_cost'] * 100:.2f}")
        print(f"  Annual Savings: ₹{cost_comparison['annual_savings'] * 100:.2f}")
        print(f"  Monthly Savings: ₹{cost_comparison['monthly_savings'] * 100:.2f}")
        print(f"  Savings Percentage: {cost_comparison['savings_percentage']}%")
        print(f"  EV Cost per km: ₹{cost_comparison['ev_cost_per_km'] * 100:.3f}")
        print(f"  ICE Cost per km: ₹{cost_comparison['ice_cost_per_km'] * 100:.3f}")
        
        # Optimal charging recommendations
        print_header("BATTERY CARE RECOMMENDATIONS")
        recommendations = ev.optimal_charging_recommendation()
        for rec in recommendations:
            print(f"  {rec}")
        
        # Summary
        print_header("SYSTEM SUMMARY")
        print(f"  Battery Capacity: {battery_capacity} kWh")
        print(f"  Current State of Health: {ev.soh:.1f}%")
        print(f"  Current Charge: {ev.current_charge}%")
        print(f"  Predicted Range: {range_data['range_km']} km")
        print(f"  Annual Fuel Savings: ₹{cost_comparison['annual_savings'] * 100:.2f}")
        
        print("\n" + "="*60)
        print("  Thank you for using EV Battery Intelligence System!")
        print("="*60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ Error: Please enter valid numeric values!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

# Run the program
if __name__ == "__main__":
    main()
    