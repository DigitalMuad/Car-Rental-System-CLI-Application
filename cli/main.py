from database.session import get_db
from models.car import Car
from models.customer import Customer
from models.rental import Rental
from sqlalchemy.orm import Session
from datetime import datetime

def display_menu():
    print("\n--- Car Rental System ---")
    print("1. Manage Cars")
    print("2. Manage Customers")
    print("3. Manage Rentals")
    print("4. Exit")

def manage_cars(db: Session):
    while True:
        print("\n--- Manage Cars ---")
        print("1. Add Car")
        print("2. Delete Car")
        print("3. View All Cars")
        print("4. Search Cars")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Car
            try:
                make = input("Enter car make: ")
                model = input("Enter car model: ")
                year = int(input("Enter car year: "))
                color = input("Enter car color: ")
                daily_rate = float(input("Enter daily rate: "))

                # Validate year
                current_year = datetime.now().year
                if year < 1900 or year > current_year:
                    print(f"Invalid year. Please enter a year between 1900 and {current_year}.")
                    continue

                # Validate daily_rate
                if daily_rate <= 0:
                    print("Daily rate must be a positive number.")
                    continue

                car = Car(make=make, model=model, year=year, color=color, daily_rate=daily_rate)
                db.add(car)
                db.commit()
                print("Car added successfully!")

            except ValueError:
                print("Invalid input. Please enter valid data.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            # Delete Car
            try:
                car_id = int(input("Enter car ID to delete: "))
                car = db.query(Car).filter(Car.id == car_id).first()
                if car:
                    db.delete(car)
                    db.commit()
                    print("Car deleted successfully!")
                else:
                    print("Car not found!")
            except ValueError:
                print("Invalid input. Please enter a valid car ID.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            # View All Cars
            cars = db.query(Car).all()
            for car in cars:
                print(car)

        elif choice == "4":
            # Search Cars
            search_term = input("Enter make or model to search: ")
            cars = db.query(Car).filter((Car.make.ilike(f"%{search_term}%")) | (Car.model.ilike(f"%{search_term}%"))).all()
            for car in cars:
                print(car)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_customers(db: Session):
    while True:
        print("\n--- Manage Customers ---")
        print("1. Add Customer")
        print("2. Delete Customer")
        print("3. View All Customers")
        print("4. Search Customers")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Customer
            try:
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                phone_number = input("Enter customer phone number: ")

                # Validate name
                if not name.strip():
                    print("Name cannot be empty. Please try again.")
                    continue

                # Validate email format
                if "@" not in email or "." not in email:
                    print("Invalid email format. Please include '@' and '.' in the email.")
                    continue

                # Validate phone number format
                if not phone_number.isdigit() or len(phone_number) < 10:
                    print("Invalid phone number. Please enter at least 10 digits.")
                    continue

                # Check if email already exists
                existing_customer = db.query(Customer).filter(Customer.email == email).first()
                if existing_customer:
                    print("A customer with this email already exists. Please use a different email.")
                    continue

                # Create and add the customer
                customer = Customer(name=name, email=email, phone_number=phone_number)
                db.add(customer)
                db.commit()
                print("Customer added successfully!")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            # Delete Customer
            try:
                customer_id = int(input("Enter customer ID to delete: "))
                customer = db.query(Customer).filter(Customer.id == customer_id).first()
                if customer:
                    db.delete(customer)
                    db.commit()
                    print("Customer deleted successfully!")
                else:
                    print("Customer not found!")
            except ValueError:
                print("Invalid input. Please enter a valid customer ID.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            # View All Customers
            customers = db.query(Customer).all()
            for customer in customers:
                print(customer)

        elif choice == "4":
            # Search Customers
            search_term = input("Enter name or email to search: ")
            customers = db.query(Customer).filter(
                (Customer.name.ilike(f"%{search_term}%")) | (Customer.email.ilike(f"%{search_term}%"))
            ).all()
            for customer in customers:
                print(customer)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_rentals(db: Session):
    while True:
        print("\n--- Manage Rentals ---")
        print("1. Rent a Car")
        print("2. Return a Car")
        print("3. View All Rentals")
        print("4. Search Rentals")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Rent a Car
            try:
                car_id = int(input("Enter car ID to rent: "))
                customer_id = int(input("Enter customer ID: "))
                rental_date = input("Enter rental date (YYYY-MM-DD): ")
                return_date = input("Enter return date (YYYY-MM-DD): ")

                # Convert dates to datetime objects
                try:
                    rental_date = datetime.strptime(rental_date, "%Y-%m-%d")
                    return_date = datetime.strptime(return_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    continue

                # Check if the car is available
                car = db.query(Car).filter(Car.id == car_id).first()
                if not car:
                    print("Car not found!")
                    continue
                if not car.is_available:
                    print("Car is not available for rent!")
                    continue

                # Check if the customer exists
                customer = db.query(Customer).filter(Customer.id == customer_id).first()
                if not customer:
                    print("Customer not found!")
                    continue

                # Validate rental duration
                rental_days = (return_date - rental_date).days
                if rental_days < 1:
                    print("Return date must be after rental date.")
                    continue

                # Calculate total cost
                total_cost = car.daily_rate * rental_days

                # Create the rental
                rental = Rental(
                    car_id=car_id,
                    customer_id=customer_id,
                    rental_date=rental_date,
                    return_date=return_date,
                    total_cost=total_cost
                )
                db.add(rental)

                # Mark the car as unavailable
                car.is_available = False
                db.commit()
                print("Car rented successfully!")

            except ValueError:
                print("Invalid input. Please enter valid data.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            # Return a Car
            try:
                rental_id = int(input("Enter rental ID to return: "))
                rental = db.query(Rental).filter(Rental.id == rental_id).first()
                if not rental:
                    print("Rental not found!")
                    continue

                # Mark the car as available
                car = db.query(Car).filter(Car.id == rental.car_id).first()
                if car:
                    car.is_available = True

                # Delete the rental record
                db.delete(rental)
                db.commit()
                print("Car returned successfully!")

            except ValueError:
                print("Invalid input. Please enter a valid rental ID.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            # View All Rentals
            rentals = db.query(Rental).all()
            for rental in rentals:
                print(rental)

        elif choice == "4":
            # Search Rentals
            search_term = input("Enter customer name or car make/model to search: ")
            rentals = db.query(Rental).join(Customer).join(Car).filter(
                (Customer.name.ilike(f"%{search_term}%")) | 
                (Car.make.ilike(f"%{search_term}%")) | 
                (Car.model.ilike(f"%{search_term}%"))
            ).all()
            for rental in rentals:
                print(rental)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    db = next(get_db())
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            manage_cars(db)
        elif choice == "2":
            manage_customers(db)
        elif choice == "3":
            manage_rentals(db)
        elif choice == "4":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()