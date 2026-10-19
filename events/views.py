from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()

    def get_queryset(self):
        query_result = self.queryset.all()
        event_status = self.request.query_params.get("status", None)
        venue = self.request.query_params.get("venue", None)
        if event_status:
            query_result = query_result.filter(status=event_status)
        if venue:
            query_result = query_result.filter(venue__icontains=venue)

        return query_result

    serializer_class = EventSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        event_id = self.request.query_params.get("event_id", None)
        if event_id:
            return self.queryset.filter(event_id=event_id)
        else:
            return self.queryset.all()

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == "cancelled": 
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Reservation already cancelled"},
            )

        event = reservation.event
        event.available_seats += reservation.seats_reserved
        reservation.status = "cancelled"
        event.save()
        reservation.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Reservation cancelled successfully",
                "event": EventSerializer(event).data,
            },
        )
