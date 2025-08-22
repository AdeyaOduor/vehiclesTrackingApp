


<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Tracking System</title>
    <!-- Material UI CSS -->
    <link href="https://unpkg.com/@material-ui/core@4.11.0/dist/material-ui.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!-- Leaflet CSS for maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</head>
<body>
    <nav class="mdc-top-app-bar">
        <div class="mdc-top-app-bar__row">
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
                <span class="mdc-top-app-bar__title">Vehicle Tracking System</span>
            </section>
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end">
                {% if user.is_authenticated %}
                <span class="mdc-top-app-bar__action-item">Welcome, {{ user.username }}</span>
                <a href="{% url 'logout' %}" class="mdc-button mdc-button--raised">Logout</a>
                {% endif %}
            </section>
        </div>
    </nav>

    <div class="mdc-drawer-app-content">
        <main class="main-content">
            <div class="mdc-top-app-bar--fixed-adjust">
                {% if messages %}
                {% for message in messages %}
                <div class="mdc-snackbar mdc-snackbar--leading">
                    <div class="mdc-snackbar__surface">
                        <div class="mdc-snackbar__label">{{ message }}</div>
                    </div>
                </div>
                {% endfor %}
                {% endif %}
                
                {% block content %}
                {% endblock %}
            </div>
        </main>
    </div>

    <!-- Material UI JS -->
    <script src="https://unpkg.com/@material-ui/core@4.11.0/dist/material-ui.min.js"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</body>
</html>


<!-- dashboard.html -->
{% extends 'base.html' %}

{% block content %}
<div class="mdc-layout-grid">
    <div class="mdc-layout-grid__inner">
        <!-- Statistics Cards -->
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>Total Vehicles</h3>
                    <h1>{{ total_vehicles }}</h1>
                </div>
            </div>
        </div>
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>Active Vehicles</h3>
                    <h1>{{ active_vehicles }}</h1>
                </div>
            </div>
        </div>
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>In Maintenance</h3>
                    <h1>{{ maintenance_vehicles }}</h1>
                </div>
            </div>
        </div>
    </div>

    <!-- Map Section -->
    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Vehicle Locations</h3>
                <div id="map" style="height: 400px;"></div>
            </div>
        </div>
    </div>

    <!-- Recent Activities -->
    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-6">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Recent Locations</h3>
                <ul class="mdc-list">
                    {% for location in recent_locations %}
                    <li class="mdc-list-item">
                        <span class="mdc-list-item__text">
                            {{ location.vehicle.license_plate }} - 
                            {{ location.latitude }}, {{ location.longitude }}
                            <span class="mdc-list-item__secondary-text">
                                {{ location.timestamp }}
                            </span>
                        </span>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>

    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-6">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Recent Work Tickets</h3>
                <ul class="mdc-list">
                    {% for ticket in recent_tickets %}
                    <li class="mdc-list-item">
                        <span class="mdc-list-item__text">
                            {{ ticket.vehicle.license_plate }} - {{ ticket.get_ticket_type_display }}
                            <span class="mdc-list-item__secondary-text">
                                Status: {{ ticket.get_status_display }}
                            </span>
                        </span>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</div>

<script>
// Initialize map
var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Fetch and plot vehicle locations
fetch('{% url "vehicle_locations" %}')
    .then(response => response.json())
    .then(data => {
        data.locations.forEach(location => {
            L.marker([location.latitude, location.longitude])
                .addTo(map)
                .bindPopup(`
                    <b>${location.vehicle}</b><br>
                    Status: ${location.status}<br>
                    Last updated: ${new Date(location.timestamp).toLocaleString()}
                `);
        });
    });
</script>
{% endblock %}
