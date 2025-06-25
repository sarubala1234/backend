from django.core.management.base import BaseCommand
from jobportal.models import Job
import random

class Command(BaseCommand):
    help = 'Set all job locations to a random Indian city.'

    def handle(self, *args, **options):
        indian_cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Bengaluru', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Pune',
            'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri',
            'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Kalyan',
            'Vasai', 'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Allahabad', 'Ranchi', 'Howrah',
            'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur', 'Kota', 'Guwahati',
            'Chandigarh', 'Solapur', 'Hubli', 'Mysore', 'Tiruchirappalli', 'Bareilly', 'Aligarh', 'Tiruppur', 'Moradabad',
            'Gurgaon', 'Noida', 'Vasai-Virar', 'Durgapur', 'Rourkela', 'Bhilai', 'Salem', 'Warangal', 'Guntur', 'Bhiwandi',
            'Saharanpur', 'Gorakhpur', 'Bikaner', 'Amravati', 'Jamshedpur', 'Bhilwara', 'Cuttack', 'Firozabad', 'Kochi',
            'Bhavnagar', 'Dehradun', 'Durg', 'Asansol', 'Nanded', 'Ajmer', 'Jamnagar', 'Ujjain', 'Sangli', 'Loni',
            'Jhansi', 'Ulhasnagar', 'Nellore', 'Jammu', 'Belgaum', 'Mangalore', 'Ambattur', 'Tirunelveli', 'Malegaon',
            'Gaya', 'Jalgaon', 'Udaipur', 'Maheshtala', 'Davanagere', 'Kozhikode', 'Kurnool', 'Rajpur Sonarpur',
            'Bokaro', 'South Dumdum', 'Bellary', 'Patiala', 'Gopalpur', 'Agartala', 'Muzaffarnagar', 'Bhatpara',
            'Panihati', 'Latur', 'Dhule', 'Rohtak', 'Korba', 'Bhilai Nagar', 'Bihar Sharif', 'Panipat', 'Darbhanga',
            'Bally', 'Aizawl', 'Dewas', 'Ichalkaranji', 'Karnal', 'Bathinda', 'Jalna', 'Eluru', 'Barasat', 'Kirari Suleman Nagar',
            'Purnia', 'Satna', 'Mau', 'Sonipat', 'Farrukhabad', 'Sagar', 'Rourkela Industrial Township', 'Durgapur',
            'Imphal', 'Ratlam', 'Hapur', 'Arrah', 'Anantapur', 'Karimnagar', 'Etawah', 'Ambernath', 'North Dumdum',
            'Bharatpur', 'Begusarai', 'New Delhi'
        ]
        jobs = Job.objects.all()
        for job in jobs:
            job.location = random.choice(indian_cities)
            job.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {jobs.count()} jobs to have random Indian city locations.')) 