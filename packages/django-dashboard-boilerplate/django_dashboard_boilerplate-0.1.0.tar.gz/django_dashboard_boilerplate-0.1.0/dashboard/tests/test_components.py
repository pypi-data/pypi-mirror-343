from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.template import Context, Template


class ComponentTests(TestCase):
    """
    Tests for dashboard components
    """
    def setUp(self):
        """
        Set up test data
        """
        self.client = Client()
        self.home_url = reverse('dashboard:home')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
    
    def test_form_field_component(self):
        """
        Test that the form_field component renders correctly
        """
        template = Template("""
            {% include 'dashboard/components/form_field.html' with 
                type="text"
                name="username"
                label="Username"
                value="testuser"
                required=True
                help_text="Your unique username"
            %}
        """)
        context = Context({})
        rendered = template.render(context)
        
        # Check that the component rendered correctly
        self.assertIn('name="username"', rendered)
        self.assertIn('value="testuser"', rendered)
        self.assertIn('required', rendered)
        self.assertIn('Your unique username', rendered)
    
    def test_modal_component(self):
        """
        Test that the modal component renders correctly
        """
        template = Template("""
            {% include 'dashboard/components/modal.html' with 
                id="test-modal"
                title="Test Modal"
                content="This is a test modal"
                primary_button="Save"
                secondary_button="Cancel"
            %}
        """)
        context = Context({})
        rendered = template.render(context)
        
        # Check that the component rendered correctly
        self.assertIn('id="test-modal"', rendered)
        self.assertIn('Test Modal', rendered)
        self.assertIn('This is a test modal', rendered)
        self.assertIn('Save', rendered)
        self.assertIn('Cancel', rendered)
    
    def test_toast_component(self):
        """
        Test that the toast component renders correctly
        """
        template = Template("""
            {% include 'dashboard/components/toast.html' with 
                id="test-toast"
                type="success"
                message="Operation completed successfully"
                duration=5000
            %}
        """)
        context = Context({})
        rendered = template.render(context)
        
        # Check that the component rendered correctly
        self.assertIn('id="test-toast"', rendered)
        self.assertIn('bg-green-500', rendered)
        self.assertIn('Operation completed successfully', rendered)
        self.assertIn('5000', rendered)
    
    def test_data_table_component(self):
        """
        Test that the data_table component renders correctly
        """
        template = Template("""
            {% include 'dashboard/components/data_table.html' with 
                id="test-table"
                headers=headers 
                rows=rows 
                sortable=True 
                searchable=True 
                pagination=True 
                items_per_page=10 
            %}
        """)
        context = Context({
            'headers': ['Name', 'Email', 'Role'],
            'rows': [
                ['John Doe', 'john@example.com', 'Admin'],
                ['Jane Smith', 'jane@example.com', 'User']
            ]
        })
        rendered = template.render(context)
        
        # Check that the component rendered correctly
        self.assertIn('id="test-table"', rendered)
        self.assertIn('Name', rendered)
        self.assertIn('Email', rendered)
        self.assertIn('Role', rendered)
        self.assertIn('John Doe', rendered)
        self.assertIn('jane@example.com', rendered)
        self.assertIn('data-sort-col', rendered)
        self.assertIn('id="test-table-search"', rendered)
        self.assertIn('id="test-table-prev"', rendered)
        self.assertIn('id="test-table-next"', rendered)
    
    def test_chart_component(self):
        """
        Test that the chart component renders correctly
        """
        template = Template("""
            {% include 'dashboard/components/chart.html' with 
                id="test-chart"
                type="line"
                title="Sales Overview"
                labels=labels
                datasets=datasets
                height=300
            %}
        """)
        context = Context({
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'datasets': [
                {
                    'label': 'Sales',
                    'data': [10, 20, 30, 40, 50],
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)'
                }
            ]
        })
        rendered = template.render(context)
        
        # Check that the component rendered correctly
        self.assertIn('id="test-chart"', rendered)
        self.assertIn('Sales Overview', rendered)
        self.assertIn('line', rendered)
        self.assertIn('300', rendered)
