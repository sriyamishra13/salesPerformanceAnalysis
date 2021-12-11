package com.pubsub.gcp.publisher;

import lombok.*;

import javax.persistence.*;

@Entity
@Table(name = "product", schema = "product_details")
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class Product {

    @Id
    @Column(name="ID",updatable=false,nullable=false)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "CONSOLE")
    public String console;

    @Column(name = "PUBLISHER")
    public String publisher;

    @Column(name = "CRITICS_POINTS")
    public Double criticsPoints;

    @Column(name = "CATEGORY")
    public String category;

    @Column(name = "RATING")
    public String rating;

    @Column(name = "USER_POINTS")
    public Integer userPoints;

    @Column(name = "YEAR")
    public Integer year;

}
