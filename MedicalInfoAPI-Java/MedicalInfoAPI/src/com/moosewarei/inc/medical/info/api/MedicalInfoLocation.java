package com.moosewarei.inc.medical.info.api;

//import java.util.ArrayList;
import java.util.List;

//import java.io.InputStream;

import javax.persistence.Query;
import javax.ws.rs.DELETE;
//import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.mooseware.inc.medical.info.model.Beacon;
import com.mooseware.inc.medical.info.model.MedicalArea;
import com.mooseware.inc.medical.info.model.MedicalAreaOfUse;
import com.mooseware.inc.medical.info.model.Patient;
import com.mooseware.inc.medical.info.model.ReasonForVisit;
import com.sun.jersey.api.client.ClientResponse.Status;

@Path("/medical_info/v1")
public class MedicalInfoLocation extends MedicalInfoBase {
	
	public MedicalInfoLocation() {
		super();
		logg.debug("MedicalInfoLocation initilized");
	}
	
	@GET
	@Path("/verify/")
	@Produces(MediaType.TEXT_PLAIN)
	public Response verifyRESTService() {
		String result = "MedicalInfo REST Successfully started..";
		return Response.status(200).entity(result).build();
	}
	
	/**
	 * Gets all of the rooms.
	 * This will need to be refined to do a search
	 * @return a list of all rooms
	 */
	@GET
	@Path("/LocationManager/rooms/")
	@Produces(MediaType.APPLICATION_JSON)	
	public Response getAllRooms() {
		String sql = "Select MEDICALAREAID, FLOOR, NAME from MEDICALAREA order by NAME, FLOOR";
		Query q = em.createNativeQuery(sql, MedicalArea.class);
		List<?> roomList = q.getResultList();
		return Response.status(Status.OK).entity(gson.toJson(roomList)).build();
	}
	
	/**
	 * Gets all of the reasons for visit.
	 * This method probably will need refinements via a search.
	 * @return a list of all reasons for visits
	 */
	@GET
	@Path("/patientManager/reasonForVisit")
	@Produces(MediaType.APPLICATION_JSON)
	public Response getAllReasonsForVisit() {
		String sql = "Select * from REASONFORVISIT order by REASONFORVISIT";
		Query q = em.createNativeQuery(sql, ReasonForVisit.class);
		List<?> reasonsList = q.getResultList();
		return Response.status(Status.OK).entity(gson.toJson(reasonsList)).build();
	}
	
	/**
	 * Gets all of the patients in the database.
	 * This method will be refined or replaced to search for names
	 * Short term:  the number of patients in the database will be limited.
	 * @return list of all patients
	 */
	@GET
	@Path("/patientManager/patients")
	@Produces(MediaType.APPLICATION_JSON)
	public Response getAllPatients() {
		String sql = "select * from PATIENT order by FAMILYNAME, GIVENNAME";
		Query q = em.createNativeQuery(sql, Patient.class);
		List<?> patientList = q.getResultList();
		return Response.status(Status.OK).entity(gson.toJson(patientList)).build();
	}
	
	//TODO:  this is open to SQL injection attack.  Need to add RE's or other means to fix
	// needed to directly concat lat/long in the query because could not get the parameter subisitution working
	// with 'POINT...
	/**
	 * Returns the patient at a specified location.
	 * If no patient at specified location, returns empty set.
	 * V1:  location error is ignored.
	 * @param latitude
	 * @param longitude
	 * @param floor
	 * @param locationErr
	 * @return Patient object
	 */
	@GET
	@Path("/LocationManager/Patient/latitude/{lat}/longitude/{long}/floor/{floor:[0-9]+}")
	@Produces(MediaType.APPLICATION_JSON)
	public Response locationManager(@PathParam("lat") String latitude,
									@PathParam("long") String longitude,
									@PathParam("floor") String floor) {
		String res = "Location manager called for corrdinates: " + latitude +  " " + longitude + "floor: " + floor;
		logg.debug(res);
		String sql = "select MEDICALAREAID, NAME from MEDICALAREA where contains(location, " +
				"GeomFromText('POINT(" + latitude + " " + longitude + ")'))" + " and floor=? limit 1";
		Query q = this.em.createNativeQuery(sql , MedicalArea.class);
		q.setParameter(1,  floor);
		Patient p = new Patient();
		try {
			MedicalArea ma = (MedicalArea) q.getSingleResult();
			if(ma == null || ma.getMedicalAreaId() == 0) {
				res = "No area of use found for " + latitude + " " + longitude;
				logg.error(res);
				return Response.status(Status.BAD_REQUEST).entity(res).build();		
			}
			sql = "select * from MEDICALAREAOFUSE where MEDAREA_MEDICALAREAID=?";
			Query medAreaUseQuery = em.createNativeQuery(sql, MedicalAreaOfUse.class);
			medAreaUseQuery.setParameter(1, ma.getMedicalAreaId());
			MedicalAreaOfUse area = (MedicalAreaOfUse) medAreaUseQuery.getSingleResult();
			if(area != null) {
				//res = "Area id: " + area.getMedicalAreaOfUseId() + " name: " + area.getName();
				p = area.getPatient();
			} else {
				res = "No patient found in room " + ma.getName();
				logg.error(res);
				//return Response.status(Status.BAD_REQUEST).entity(res).build();
				return Response.status(Status.BAD_REQUEST).build();
			}
		} catch (Exception e) {
			logg.error("Unable to find area for coordinates of: " + latitude + " " + longitude);
			res = "No area of use found for " + latitude + " " + longitude;
			//return Response.status(Status.BAD_REQUEST).entity(res).build();
			return Response.status(Status.BAD_REQUEST).build();
		}
		return Response.status(200).entity(gson.toJson(p)).build();
	}
	
	/**
	 * Returns the patient resources for the patient with in 1.5m of the beacon.
	 * Distance is selected on the ipad via Apple's location manager
	 */
	@GET
	@Path("/LocationManager/Beacon/{uuid}/major/{major:[0-9]+}/minor/{minor:[0-9]+}")
	@Produces(MediaType.APPLICATION_JSON)
	public Response getPatientInRoom(@PathParam("uuid") String beaconUuid,
									@PathParam("major") String major,
									@PathParam("minor") String minor) {
		String sql = "select * from BEACON where uuid='" + beaconUuid +
				"' and major=" + major + " and minor=" + minor;
		try {
			Query q = em.createNativeQuery(sql, Beacon.class);
			Beacon b = (Beacon) q.getSingleResult();
			sql = "select MEDICALAREAID, FLOOR, NAME from MEDICALAREA where BEACON_BEACONID=" + b.getBeaconId();
			q= em.createNativeQuery(sql, MedicalArea.class);
			MedicalArea ma = (MedicalArea) q.getSingleResult();
			ma.setBeacon(b);
			sql = "select * from MEDICALAREAOFUSE where MEDAREA_MEDICALAREAID=" + ma.getMedicalAreaId();
			q = em.createNativeQuery(sql, MedicalAreaOfUse.class);
			MedicalAreaOfUse mau = (MedicalAreaOfUse) q.getSingleResult();
			return Response.status(Status.OK).entity(gson.toJson(mau.getPatient())).build();
		} catch (Exception e) {
			logg.error("Error getting beacon: " + e.getMessage());
			logg.error("SQL: " + sql);
		}
		return Response.status(Status.BAD_REQUEST).build();
	}
	
	/**
	 * 
	 * @return all of the active UUID's  Apple's iBeacons use these to define regions
	 */
	@GET
	@Path("/LocationManager/Beacon/")
	@Produces(MediaType.APPLICATION_JSON)
	public Response getRegions() {
		String sql = "select * from BEACON order by UUID, MAJOR, MINOR";
		try {
			Query q = em.createNativeQuery(sql, Beacon.class);
			List<?> beaconList = q.getResultList();
			return Response.status(Status.OK).entity(gson.toJson(beaconList)).build();
		} catch(Exception e) {
			logg.error("Error attempting to get beacon list: " + e.getMessage());
		}		
		return Response.status(Status.BAD_REQUEST).build();
	}
	
	@DELETE
	@Path("/LocationManager/patient/{patientId:[0-9]+}")
	@Produces(MediaType.APPLICATION_JSON)
	public Response removePatientFromRoom(@PathParam("patientId") String patientId) {
		try {
			String sql = "delete from MEDICALAREAOFUSE where PATIENT_PATIENTID=?";
			Query q = em.createNativeQuery(sql);
			q.setParameter(1, Integer.parseInt(patientId));
			em.getTransaction().begin();
			q.executeUpdate();
			em.getTransaction().commit();
		} catch(Exception e) {
			logg.error("Unable to remove patient from area with patient id " + patientId + " for reason: " + e.getMessage());
			return Response.status(Status.BAD_REQUEST).build();
		}
		return Response.status(Status.ACCEPTED).build();
	}
	
	@POST
	@Path("/LocationManager/Patient/{patientId:[0-9]+}/room/{roomId:[0-9]+}/reasonForVisit/{reasonForVisitCode:[0-9]+}")
	@Produces(MediaType.APPLICATION_JSON)
	public Response putPatientInRoom(@PathParam("patientId") String patientId, 
									@PathParam("roomId") String roomId,
									@PathParam("reasonForVisitCode") String visitCode){
		MedicalAreaOfUse mau = new MedicalAreaOfUse();
		try{
			String sql = "select MEDICALAREAID, FLOOR, NAME from MEDICALAREA where MEDICALAREAID=?";
			Query medAreaQuery = em.createNativeQuery(sql,  MedicalArea.class);
			medAreaQuery.setParameter(1,  Integer.parseInt(roomId));
			MedicalArea medArea = (MedicalArea) medAreaQuery.getSingleResult();
			sql = "select * from MEDICALAREAOFUSE where MEDAREA_MEDICALAREAID=?";
			Query q = em.createNativeQuery(sql, MedicalAreaOfUse.class);
			q.setParameter(1,  Integer.parseInt(roomId));
			MedicalAreaOfUse mauTemp = new MedicalAreaOfUse();
			ReasonForVisit visit = em.find(ReasonForVisit.class, Integer.parseInt(visitCode));
			try {
				mauTemp = (MedicalAreaOfUse) q.getSingleResult();
			} catch (Exception e) {
				logg.info("Unable to get medical area of use for id: " + roomId);
			}
			if(mauTemp.getPatient() != null) {
				logg.error("Attempt to assign patient to a non-empty room");
				return Response.status(Status.CONFLICT).entity("Patient already in room").build();
			}
			Patient p = new Patient();
			try {
				p = this.em.find(Patient.class, Integer.parseInt(patientId));
			} catch (Exception e) {
				logg.error("Unable to find patient w/ ID of: " + patientId);
				return Response.status(Status.BAD_REQUEST).entity("Bad patient id").build();
			}
			mau.setPatient(p);
			mau.setMedArea(medArea);
			mau.setReasonForVisit(visit);
			this.em.getTransaction().begin();
			em.persist(mau);
			this.em.getTransaction().commit();
		} catch (Exception e) {
			this.logg.error("Failed to put patient in room: " + e.getMessage());
			return Response.status(Status.INTERNAL_SERVER_ERROR).build();
		}
		return Response.status(Status.ACCEPTED).entity(gson.toJson(mau)).build();
	}
}
